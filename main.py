import github
import file
import summary
import json


def main():
    # Get the repository URL from user input
    repo_url = input("Enter the repository URL: ")

    # Extract the repository owner and name from the URL
    repo_owner = repo_url.split("/")[-2]
    repo_name = repo_url.split("/")[-1]

    print("Retrieving files from " + repo_owner + "/" + repo_name + "...")
    # Retrieve Github repository contents
    url = "https://github.com/" + repo_owner + "/" + repo_name
    file_infos = github.get_files_in_folder(url, repo_owner, repo_name)

    with open("output.txt", "a") as f:
        f.write("FILE INFOS:\n")
        for file_info in file_infos:
            f.write(str(file_info) + "\n")

    # Summarize the contents of each file
    summaries = []
    for file_info in file_infos:
        print("Summarizing " + file_info["name"] + "...")
        content = file.get_file_content(file_info["path"])
        summary_text = json.dumps(summary.summarize_content(content))
        print(type(summary_text))
        print(summary_text)
        summaries.append(summary_text)

    # Write the summaries to a file
    with open("output.txt", "a") as f:
        f.write("SUMMARIES:\n")
        for summary_text in summaries:
            f.write(summary_text + "\n")


if __name__ == '__main__':
    main()
