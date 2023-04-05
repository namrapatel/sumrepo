import github
import gpt
import json
import utils


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

    with open("output.txt", "w") as f:
        f.write("Files information:\n")
        for file_info in file_infos:
            f.write(str(file_info) + "\n")

    # Summarize the contents of each file
    summarized_files = []
    for file_info in file_infos:
        print("Summarizing " + file_info["name"] + "...")
        path =  utils.get_path_from_url(file_info["url"], repo_owner)
        url = utils.get_file_content(file_info["url"])
        content = "File name: {}\nFile path: {}\nCode:\n{}\n".format(
            file_info["name"],
            path,
            url
        )
        summary_text = json.dumps(gpt.summarize_file(content))
        summarized_files.append({"name": file_info["name"], "path": path, "summary": summary_text})

    # Write the summaries to a file
    with open("output.txt", "w") as f:
        f.write("Summaries:\n")
        for line in summarized_files:
            f.write(f"{line['name']}: {line['summary']}\n")

    # Make another chat completion request to summarize the summaries
    print("Summarizing the summaries...")
    summary_text = ""
    for line in summarized_files:
        summary_text += line["summary"] + "\n"
    summary_text = json.dumps(gpt.summarize_summaries(summary_text)) 




if __name__ == '__main__':
    main()