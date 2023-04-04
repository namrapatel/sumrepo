import { useState } from 'react';
import { File } from './types';
import { getRepositoryFiles } from './api';

function App() {
  const [repositoryUrl, setRepositoryUrl] = useState('');
  const [files, setFiles] = useState<File[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleSubmit = async (event: React.FormEvent<HTMLFormElement>) => {
    event.preventDefault();

    setIsLoading(true);
    setError(null);

    try {
      const files = await getRepositoryFiles(repositoryUrl);
      setFiles(files);
    } catch (error) {
      // setError(error.message);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div>
      <h1>GitHub Repo Explorer</h1>

      <form onSubmit={handleSubmit}>
        <input type="text" value={repositoryUrl} onChange={event => setRepositoryUrl(event.target.value)} placeholder="Enter a GitHub repository URL" />
        <button type="submit">Explore Repository</button>
      </form>

      {isLoading && <p>Loading...</p>}
      {error && <p>Error: {error}</p>}
      {files.length > 0 && (
        <ul>
          {files.map(file => (
            <li key={file.path}>{file.name} ({file.type})</li>
          ))}
        </ul>
      )}
    </div>
  );
}

export default App;
