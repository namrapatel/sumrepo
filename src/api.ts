import { File } from './types';
  
export async function getRepositoryFiles(repositoryUrl: string, accessToken?: string): Promise<File[]> {
    const apiUrl = `https://api.github.com/repos/${repositoryUrl}/contents`;
  
    const response = await fetch(apiUrl, {
      headers: {
        Authorization: accessToken ? `token ${accessToken}` : ''
      }
    });

    if (!response.ok) {
        throw new Error(`Failed to retrieve repository files: ${response.status}`);
    }

    const fileData = await response.json();

    const files = fileData.map((file: File) => ({
        name: file.name,
        path: file.path,
        downloadUrl: file.downloadUrl,
        type: file.type
    }));

    return files;
}
  