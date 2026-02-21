// Background service worker for Slop Scan
chrome.runtime.onInstalled.addListener(() => {
  console.log('Slop Scan extension installed');
});

chrome.runtime.onMessage.addListener(
  (request: { action: string }, _sender: chrome.runtime.MessageSender, sendResponse: (response?: any) => void) => {
    if (request.action === 'processScan') {
      sendResponse({ status: 'processed' });
    }
  }
);
