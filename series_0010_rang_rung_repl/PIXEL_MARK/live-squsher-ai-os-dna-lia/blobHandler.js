// blobHandler.js

// Store blobs in a map with directory structure
const blobs = new Map();

// Function to get a Blob from a URL or filename with directory support
function getBlobFromURLOrFilename(urlOrFilename) {
  // Check if the input contains directory structure
  if (urlOrFilename.includes('/')) {
    const [directory, filename] = urlOrFilename.split('/');

    // Check if the directory exists in the blobs map
    if (!blobs.has(directory)) {
      console.error(`Directory not found: ${directory}`);
      return null;
    }

    const dirBlobs = blobs.get(directory);

    // Check if the file exists in the directory
    if (!dirBlobs.has(filename)) {
      console.error(`File not found: ${filename} in directory ${directory}`);
      return null;
    }

    return dirBlobs.get(filename);
  } else {
    // Handling for other file types (outside directory structure)
    const fileExtension = urlOrFilename.split('.').pop().toLowerCase();

    switch(fileExtension) {
      case 'mp4':
        // Existing MP4 handling
        return handleMP4(urlOrFilename);
      case 'mp3':
      case 'avi':
      case 'mkv':
      case 'jpg':
      case 'png':
      case 'gif':
        // Common handling for all supported file types
        if (blobs.has(urlOrFilename)) {
          return blobs.get(urlOrFilename);
        } else {
          console.error(`File not found: ${urlOrFilename}`);
        }
        break;
      default:
        console.error(`Unsupported file type: ${fileExtension}`);
    }
  }
}

// Add a Blob to the map
function addBlob(urlOrFilename, blobData) {
  blobs.set(urlOrFilename, blobData);
}

// Existing MP4 handling function
function handleMP4(urlOrFilename) {
  // Check if the MP4 file exists in the blobs map
  if (blobs.has(urlOrFilename)) {
    // Retrieve and return the MP4 blob
    return blobs.get(urlOrFilename);
  } else {
    // Log an error if the file is not found
    console.error(`MP4 file not found: ${urlOrFilename}`);
    return null;
  }
}

// Function to get all blob filenames
function getAllBlobFilenames() {
  return Array.from(blobs.keys());
}

// Export the blobs map and relevant functions
export { blobs, getBlobFromURLOrFilename, addBlob, getAllBlobFilenames };
