// Background service worker for Slop Scan
chrome.runtime.onInstalled.addListener(() => {
  console.log('Slop Scan extension installed');
});

chrome.runtime.onMessage.addListener(
  (request: { action: string; filename?: string; content?: string; images?: string[] }, _sender: chrome.runtime.MessageSender, sendResponse: (response?: any) => void) => {
    if (request.action === 'downloadFile' && request.filename && request.content) {
      // Download text file
      const blob = new Blob([request.content], { type: 'text/plain' })
      const url = URL.createObjectURL(blob)
      
      chrome.downloads.download(
        {
          url,
          filename: request.filename,
          saveAs: true,
        },
        () => {
          // Download images
          if (request.images && request.images.length > 0) {
            request.images.forEach((imgUrl: string, index: number) => {
              try {
                // Only download valid URLs
                if (imgUrl.startsWith('http://') || imgUrl.startsWith('https://') || imgUrl.startsWith('data:')) {
                  const timestamp = new Date().toISOString().slice(0, 19).replace(/:/g, '-')
                  const ext = imgUrl.split('.').pop()?.split('?')[0] || 'jpg'
                  chrome.downloads.download({
                    url: imgUrl,
                    filename: `images/image-${timestamp}-${index}.${ext}`,
                  })
                }
              } catch (e) {
                console.error('Error downloading image:', imgUrl, e)
              }
            })
          }
          
          sendResponse({ success: true, message: `Downloaded ${request.images?.length || 0} images` })
        }
      )
    } else if (request.action === 'processScan') {
      sendResponse({ status: 'processed' })
    }
  }
);
