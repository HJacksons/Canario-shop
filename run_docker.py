import subprocess


def run_docker_container():
    cmd = [
        "docker", "run",
        "--name", "canario-shop",
        "-p", "8000:80",
        "-e", "SHOW_FLASHSALE=0",
        "-e", "SHOW_PREMIUM=1",
        "-e", "USE_MEMCACHE=Y",
        "-e", "MEMCACHE_SERVER=10.196.38.192", #host.docker.internal
        "-d", "canario-shop:latest"
    ]

    subprocess.run(cmd)


if __name__ == "__main__":
    run_docker_container()
