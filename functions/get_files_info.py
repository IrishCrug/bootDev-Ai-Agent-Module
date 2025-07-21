import os
def get_files_info(working_directory, directory="."):

    try:
        full_path = os.path.join(working_directory, directory)
        abso_path = os.path.abspath(full_path)
        working_abs = os.path.abspath(working_directory)


        if not (abso_path == working_abs or abso_path.startswith(working_abs + os.sep)):
            return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
        else:
            if not os.path.isdir(abso_path):
                return f'Error: "{directory}" is not a directory'
            else:
                direc_contents_list = os.listdir(full_path)
                return_string_list = []
                for dic in direc_contents_list:
                    file_name = dic
                    dic_path = os.path.join(full_path, dic)
                    file_size = os.path.getsize(dic_path)
                    file_or_dir = os.path.isdir(dic_path)
                    return_string_list.append(f"- {file_name}: file_size={file_size} bytes, is_dir={file_or_dir}")
                return_string = "\n".join(return_string_list)
                return return_string
    except Exception as e:
        return f"Error: {str(e)}"