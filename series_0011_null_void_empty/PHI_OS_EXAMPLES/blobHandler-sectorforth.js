// blobHandler-sectorforth.js - Purified Version

const blobs = new Map();

function getBlobFromURLOrFilename(urlOrFilename) {
  if (urlOrFilename.includes('/')) {
    const [directory, filename] = urlOrFilename.split('/');
    if (!blobs.has(directory)) return null;
    const directoryBlobs = blobs.get(directory);
    return directoryBlobs.get(filename) || null;
  } else {
    return blobs.get(urlOrFilename) || null;
  }
}

function createObjectURLInDirectory(blob, directory, filename) {
  if (blob instanceof Blob) {
    const objectURL = URL.createObjectURL(blob);
    if (!blobs.has(directory)) {
      blobs.set(directory, new Map());
    }
    blobs.get(directory).set(objectURL, blob);
    blobs.get(directory).set(filename, blob);
    return objectURL;
  }
  return null;
}

function handleScriptResourceRequest(scriptName, resourcePath) {
  const fullResourcePath = `${scriptName}/${resourcePath}`;
  const blob = getBlobFromURLOrFilename(fullResourcePath);
  return blob ? URL.createObjectURL(blob) : null;
}

function getMp4Files() {
  const mp4Files = [];
  blobs.forEach((directoryBlobs) => {
    directoryBlobs.forEach((blob, key) => {
      if (blob.type === 'video/mp4') {
        mp4Files.push({ name: key, url: URL.createObjectURL(blob) });
      }
    });
  });
  return mp4Files;
}

function autoPlayVideos() {
    const mp4Files = getMp4Files();
    let currentVideoIndex = 0;
    const videoPlayer = document.getElementById('videoPlayer');
    if (!videoPlayer) return;

    function playNextVideo() {
        if (currentVideoIndex < mp4Files.length) {
            videoPlayer.src = mp4Files[currentVideoIndex].url;
            videoPlayer.play();
            currentVideoIndex++;
        }
    }
    videoPlayer.onended = playNextVideo;
    playNextVideo();
}

export { getBlobFromURLOrFilename, createObjectURLInDirectory, handleScriptResourceRequest, getMp4Files, autoPlayVideos };