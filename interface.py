#!-*-coding:utf-8-*-
import schemaManager
import apiOS

PROGRAM_NAME = u'DataAnalysis'


class StatusMessage:
    PROJECT_NO_OPEN = 0
    PROJECT_OPEN = 1
    PROJECT_NO_SAVE = 2
    PROJECT_SAVE = 3
    PROJECT_NO_SAVE_AS = 4
    PROJECT_SAVE_AS = 5
    PROJECT_NO_CREATE = 6
    PROJECT_CREATE = 7
    PROJECT_NO_EXIST = 8
    PROJECT_NO_CLOSE = 9
    PROJECT_CLOSE = 10
    FILE_PROJECT_NO_SELECT = 11

    MESSAGES = [u'Проект не удалось открыть',
                u'Проект открыт',
                u'Проект не удалось сохранить',
                u'Проект сохранен',
                u'Проект не удалось сохранить',
                u'Проект сохранен как',
                u'Проект не удалось создать',
                u'Проект создан',
                u'Проект eще не создан',
                u'Проект не удалось закрыть',
                u'Проект закрыт',
                u'Файл проекта не выбран',
                u'']

    def __init__(self):
        pass

    def get_message_text(self, code_message):
        return self.MESSAGES[code_message]


def set_program_status(main_window, message, addition_text=None):
    message_text = message
    if addition_text:
        message_text += ': ' + addition_text

    main_window.statusBar().showMessage(message_text)


def set_title_main_window(main_window, title):
    window_title = PROGRAM_NAME + \
                   u' - ' + \
                   unicode(title)

    main_window.setWindowTitle(window_title)


def create_new_schema(main_window, active_schema):
    api = apiOS.ApiOS()

    try:
        if is_schema_need_saving(active_schema):
            api.show_save_schema_dialog(main_window)

        new_schema_path = apiOS.ApiOS().show_create_schema_dialog(main_window)

        if new_schema_path:
            new_schema = schemaManager.get_new_schema(None, new_schema_path)
            set_program_status(main_window, StatusMessage().get_message_text(StatusMessage().PROJECT_CREATE),
                               unicode(new_schema_path))

            return new_schema
        else:
            return None

    except IndexError:
        set_program_status(main_window, StatusMessage().PROJECT_NO_CREATE)
        return None


def is_schema_need_saving(active_schema):
    if active_schema:
        return True

    return False


def show_dialog_for_save_schema(active_schema):
    api = apiOS.ApiOS()

    try:
        if is_schema_need_saving(active_schema):
            variant_to_save = api.show_variants_to_save_schema()

            if variant_to_save == api.VARIANT_SAVE_SCHEMA:
                file_path = active_schema.get_file_path()

                if file_path and schemaManager.save_schema_in_file(active_schema, file_path):
                    return api.VARIANT_SAVE_SCHEMA

                return api.VARIANT_CANCEL

            return variant_to_save
        else:
            return api.VARIANT_NO_SAVE_SCHEMA

    except IndexError:
        return api.VARIANT_CANCEL


def save_schema(main_window, active_schema):
    api = apiOS.ApiOS()
    message_box = StatusMessage()

    if active_schema:
        if schemaManager.save_schema_in_file(active_schema, active_schema.get_file_path()):
            set_program_status(main_window,
                               message_box.get_message_text(message_box.PROJECT_SAVE),
                               active_schema.get_file_path())
        else:
            set_program_status(main_window,
                               message_box.get_message_text(message_box.PROJECT_NO_SAVE),
                               active_schema.get_file_path())
    else:
        set_program_status(main_window, message_box.get_message_text(message_box.PROJECT_NO_EXIST))
        api.send_system_message(api.MESSAGE_WARNING, message_box.get_message_text(message_box.PROJECT_NO_EXIST))


def open_schema(main_window, active_schema):
    api = apiOS.ApiOS()
    message_box = StatusMessage()

    if show_dialog_for_save_schema(active_schema) != api.VARIANT_CANCEL:

        schema_file_path = api.show_open_schema_dialog(main_window)

        if schema_file_path:
            load_schema = schemaManager.load_schema_from_file(schema_file_path)

            set_program_status(main_window,
                               message_box.get_message_text(message_box.PROJECT_OPEN),
                               schema_file_path)

            return load_schema

        else:
            set_program_status(main_window,
                               message_box.get_message_text(message_box.PROJECT_NO_OPEN),
                               schema_file_path)
    else:
        return active_schema


def save_schema_as(main_window, active_schema):
    api = apiOS.ApiOS()
    message_box = StatusMessage()

    if active_schema:
        new_schema_file_path = api.show_create_schema_dialog(main_window)

        if new_schema_file_path:
            active_schema.set_file_path(new_schema_file_path)
            if schemaManager.save_schema_in_file(active_schema, new_schema_file_path):
                set_program_status(main_window, message_box.get_message_text(message_box.PROJECT_SAVE_AS),
                                   new_schema_file_path)
                return True

        api.send_system_message(api.MESSAGE_WARNING, message_box.get_message_text(message_box.PROJECT_NO_SAVE_AS))
    else:
        set_program_status(main_window, message_box.get_message_text(message_box.PROJECT_NO_EXIST))
        api.send_system_message(api.MESSAGE_WARNING, message_box.get_message_text(message_box.PROJECT_NO_EXIST))

    return False


def close_schema(main_window, active_schema):
    api = apiOS.ApiOS()
    message_box = StatusMessage()

    if show_dialog_for_save_schema(active_schema) != api.VARIANT_CANCEL:
        set_program_status(main_window,
                           message_box.get_message_text(message_box.FILE_PROJECT_NO_SELECT))
        return None
    else:
        set_program_status(main_window,
                           message_box.get_message_text(message_box.PROJECT_NO_CLOSE),
                           active_schema.get_file_path())

        return active_schema
