// Content script for Slop Scan
console.log('Slop Scan content script loaded');

interface ScrapedData {
  texts: string[]
  images: string[]
  totalTexts: number
  totalImages: number
}

const scrapePageContent = (): ScrapedData => {
  const texts: string[] = []
  const images: string[] = []

  // Extract all text content
  const bodyText = document.body.innerText
  if (bodyText.trim()) {
    texts.push(bodyText.trim())
  }

  // Extract all text from paragraphs
  const paragraphs = document.querySelectorAll('p')
  paragraphs.forEach((p) => {
    const text = (p as HTMLElement).innerText?.trim()
    if (text) {
      texts.push(text)
    }
  })

  // Extract all text from headings
  const headings = document.querySelectorAll('h1, h2, h3, h4, h5, h6')
  headings.forEach((h) => {
    const text = (h as HTMLElement).innerText?.trim()
    if (text) {
      texts.push(text)
    }
  })

  // Extract all text from divs with text content
  const divs = document.querySelectorAll('div')
  divs.forEach((div) => {
    const text = (div as HTMLElement).innerText?.trim()
    if (text && text.length < 500) {
      texts.push(text)
    }
  })

  // Extract all image sources
  const imgElements = document.querySelectorAll('img')
  imgElements.forEach((img) => {
    const src = (img as HTMLImageElement).src || img.getAttribute('data-src')
    if (src) {
      images.push(src)
    }
  })

  // Extract background images from CSS
  const allElements = document.querySelectorAll('*')
  allElements.forEach((el) => {
    const style = window.getComputedStyle(el)
    const bgImage = style.backgroundImage
    if (bgImage && bgImage !== 'none') {
      const url = bgImage.match(/url\(['"]?([^'")]+)['"]?\)/)
      if (url && url[1]) {
        images.push(url[1])
      }
    }
  })

  // Remove duplicates
  const uniqueTexts = Array.from(new Set(texts))
  const uniqueImages = Array.from(new Set(images))

  return {
    texts: uniqueTexts,
    images: uniqueImages,
    totalTexts: uniqueTexts.length,
    totalImages: uniqueImages.length,
  }
}

chrome.runtime.onMessage.addListener(
  (request: { action: string }, _sender: chrome.runtime.MessageSender, sendResponse: (response?: any) => void) => {
    if (request.action === 'scrapePage') {
      const scrapedData = scrapePageContent()
      sendResponse(scrapedData)
    } else if (request.action === 'downloadScrapedData') {
      const scrapedData = scrapePageContent()
      const timestamp = new Date().toISOString().slice(0, 19).replace(/:/g, '-')
      const filename = `scraped-${timestamp}.txt`
      
      // Create text content
      const textContent = `Scraped Content - ${new Date().toLocaleString()}
${'='.repeat(50)}

TEXT CONTENT (${scrapedData.totalTexts} blocks):
${'-'.repeat(50)}
${scrapedData.texts.join('\n\n')}`
      
      // Send to background script to download
      chrome.runtime.sendMessage(
        { action: 'downloadFile', filename, content: textContent, images: scrapedData.images },
        (response) => {
          sendResponse({ success: true, message: response.message })
        }
      )
    } else if (request.action === 'scanPage') {
      sendResponse({ status: 'scanning' })
    }
  }
);
