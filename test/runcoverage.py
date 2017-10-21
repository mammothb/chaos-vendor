import os
import subprocess

def main():
    current_dir = os.path.dirname(os.path.realpath(__file__))
    test_file = os.path.join(current_dir, "testall.py")
    subprocess.call(["coverage", "run", test_file], cwd=current_dir)
    subprocess.call(["coverage", "html"], cwd=current_dir)

if __name__ == "__main__":
    main()
