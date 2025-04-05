import os




def shell_cmd(cmd: str) -> str:
    """执行 shell 命令并返回其输出。
    
    Args:
        cmd (str): 要执行的 shell 命令，例如 "ls -l"（Linux/macOS）或 "dir"（Windows）。

    Returns:
        str: 命令执行的标准输出内容。如果命令无输出或执行失败，可能返回空字符串。

    Raises:
        OSError: 如果命令无法执行（例如命令不存在或权限不足）。
        TypeError: 如果传入的 `cmd` 参数不是字符串。
    """
    return os.popen(cmd).read()






