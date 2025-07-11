import os

def create_frontend_structure():
    """
    Creates the frontend directory structure with specified subdirectories and empty files.
    """
    base_dir = "frontend"

    # Define the directory structure
    dirs = [
        os.path.join(base_dir, "css"),
        os.path.join(base_dir, "js"),
        os.path.join(base_dir, "assets", "images"),
        os.path.join(base_dir, "assets", "fonts")
    ]

    # Define the files to create
    files = [
        os.path.join(base_dir, "index.html"),
        os.path.join(base_dir, "login.html"),
        os.path.join(base_dir, "register.html"),
        os.path.join(base_dir, "predict.html"),
        os.path.join(base_dir, "help.html"),
        os.path.join(base_dir, "README.md"),
        os.path.join(base_dir, "css", "style.css"),
        os.path.join(base_dir, "js", "main.js"),
        os.path.join(base_dir, "js", "auth.js"),
        os.path.join(base_dir, "js", "prediction.js")
    ]

    print(f"Creating frontend project structure in '{base_dir}/'...")

    # Create directories
    for d in dirs:
        os.makedirs(d, exist_ok=True)
        print(f"Created directory: {d}")

    # Create empty files
    for f in files:
        with open(f, "w") as file:
            pass # Create an empty file
        print(f"Created file: {f}")

    print("\nFrontend structure created successfully!")
    print("You can now navigate into the 'frontend' directory and start adding content.")

if __name__ == "__main__":
    create_frontend_structure()