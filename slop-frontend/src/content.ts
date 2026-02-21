// Content script for Slop Scan
console.log('Slop Scan content script loaded');

chrome.runtime.onMessage.addListener(
  (request: { action: string }, _sender: chrome.runtime.MessageSender, sendResponse: (response?: any) => void) => {
    if (request.action === 'scanPage') {
      sendResponse({ status: 'scanning' });
    }
  }
);
