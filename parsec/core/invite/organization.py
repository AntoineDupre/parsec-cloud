# Parsec Cloud (https://parsec.cloud) Copyright (c) AGPLv3 2019 Scille SAS

from typing import Optional
from pendulum import now as pendulum_now

from parsec.crypto import SigningKey
from parsec.api.data import UserCertificateContent, DeviceCertificateContent, UserProfile
from parsec.api.protocol import HumanHandle, DeviceID
from parsec.core.types import LocalDevice, BackendOrganizationAddr
from parsec.core.local_device import generate_new_device
from parsec.core.backend_connection import APIV1_BackendAnonymousCmds


async def bootstrap_organization(
    cmds: APIV1_BackendAnonymousCmds,
    human_handle: Optional[HumanHandle],
    device_label: Optional[str],
) -> LocalDevice:
    root_signing_key = SigningKey.generate()
    root_verify_key = root_signing_key.verify_key

    organization_addr = BackendOrganizationAddr.build(
        backend_addr=cmds.addr,
        organization_id=cmds.addr.organization_id,
        root_verify_key=root_verify_key,
    )

    device = generate_new_device(
        device_id=DeviceID.new(),
        organization_addr=organization_addr,
        profile=UserProfile.ADMIN,
        human_handle=human_handle,
        device_label=device_label,
    )

    now = pendulum_now()
    user_certificate = UserCertificateContent(
        author=None,
        timestamp=now,
        user_id=device.user_id,
        public_key=device.public_key,
        profile=device.profile,
    )
    redacted_user_certificate = user_certificate.evolve(human_handle=None)
    device_certificate = DeviceCertificateContent(
        author=None, timestamp=now, device_id=device.device_id, verify_key=device.verify_key
    )
    redacted_device_certificate = device_certificate.evolve(device_label=None)

    user_certificate = user_certificate.dump_and_sign(root_signing_key)
    redacted_user_certificate = redacted_user_certificate.dump_and_sign(root_signing_key)
    device_certificate = device_certificate.dump_and_sign(root_signing_key)
    redacted_device_certificate = redacted_device_certificate.dump_and_sign(root_signing_key)

    await cmds.organization_bootstrap(
        organization_id=cmds.addr.organization_id,
        bootstrap_token=cmds.addr.token,
        root_verify_key=root_verify_key,
        user_certificate=user_certificate,
        device_certificate=device_certificate,
        redacted_user_certificate=redacted_user_certificate,
        redacted_device_certificate=redacted_device_certificate,
    )

    return device
