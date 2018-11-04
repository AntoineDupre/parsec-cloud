# Used only for translations

SOURCES += app.py \
           main_window.py \
           files_widget.py \
           login_widget.py \
           settings_widget.py \
           users_widget.py \
           file_size.py \
           item_widget.py \
           custom_widgets.py \
           devices_widget.py \
           workspaces_widget.py \


TRANSLATIONS += tr/parsec_fr.ts \
                tr/parsec_es.ts \
                tr/parsec_de.ts \
                tr/parsec_en.ts \
                tr/parsec_zh.ts


FORMS += forms/main_window.ui \
         forms/files_widget.ui \
         forms/users_widget.ui \
         forms/settings_widget.ui \
         forms/file_item_widget.ui \
         forms/parent_item_widget.ui \
         forms/login_widget.ui \
         forms/register_device.ui \
         forms/devices_widget.ui \
         forms/login_login_widget.ui \
         forms/login_register_device_widget.ui \
         forms/login_register_user_widget.ui \
         forms/mount_widget.ui \
         forms/workspaces_widget.ui \
         forms/workspace_button.ui \
         forms/folder_item_widget.ui \
         forms/message_dialog.ui \
         forms/user_button.ui \
         forms/input_dialog.ui \
         forms/question_dialog.ui

RESOURCES += rc/resources.qrc

HEADERS += \
    forms/inputdialog.h \
    forms/questiondialog.h
