import os
import hashlib
import requests

default_urls = {
    "ckg_latest_4.2.3.dump": "https://data.mendeley.com/public-files/datasets/mrcf7f4tc2/files/ffaab45e-e15c-412d-b63b-5df681a2e303/file_downloaded",
    "data.zip": "https://data.mendeley.com/public-files/datasets/mrcf7f4tc2/files/69de0ef6-6e71-4d8e-8fbc-b933b9fc4dce/file_downloaded"
}

default_md5 = {
    "ckg_latest_4.2.3.dump": "eebe895e2e9f9fc39f3663fbcea032d5",
    "data.zip": "1bbd8be31efcd559244b26f474d9ad59"
}

def read_dict(file_path, abs_path=True): # Helper function to read md5sum output
    file_dict = {}
    with open(file_path, 'r') as file:
        for line in file:
            parts = line.strip().split("  ", 1)
            if len(parts) == 2:
                value, filename = parts
                if abs_path:
                    filename = os.path.abspath(filename)
                else:
                    filename = os.path.basename(filename)
                file_dict[filename] = value
    return file_dict

def download_file(url, file_path):
    hash_md5 = hashlib.md5()
    response = requests.get(url, stream=True)
    response.raise_for_status()  # Ensure we raise an error for bad status codes
    with open(file_path, "wb") as f:
        for chunk in response.iter_content(chunk_size=8192):
            if chunk:
                f.write(chunk)
                hash_md5.update(chunk)
    return hash_md5.hexdigest()

def main():
    if os.path.exists("./ckg_latest.md5"):
        expected_md5 = read_dict("./ckg_latest.md5")
    else:
        expected_md5 = default_md5
    if os.path.exists("./ckg_latest.urls"):
        urls = read_dict("./ckg_latest.urls")
    else:
        urls = default_urls

    for file_name, url in urls.items():
        if os.path.exists(file_name):
            actual_md5 = hashlib.md5(open(file_name, "rb").read()).hexdigest()
            if actual_md5 == expected_md5[file_name]:
                print(f"{file_name} exists and MD5 matches. Skipping download.")
                continue
            else:
                print(f"{file_name} exists but MD5 does not match. Re-downloading.")
        else:
            print(f"{file_name} does not exist. Downloading.")
        actual_md5 = download_file(url, file_name)
        if actual_md5 == expected_md5[file_name]: 
            print(f"{file_name} downloaded and MD5 matches.")
        else:
            print(f"Error: {file_name} downloaded but MD5 does not match.")

if __name__ == "__main__":
    main()
