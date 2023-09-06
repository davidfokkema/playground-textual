import subprocess

with subprocess.Popen(
    "pip install --force numpy --no-cache",
    shell=True,
    stdout=subprocess.PIPE,
    encoding="utf-8",
) as proc:
    while True:
        output = proc.stdout.readline()
        if output == "" and proc.poll() is not None:
            break
        print(output, end="")
