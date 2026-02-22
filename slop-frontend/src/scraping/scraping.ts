export interface ScrapedData {
  texts: string[]
  images: string[]
  totalTexts: number
  totalImages: number
}

/**
 * Scrapes all text and images from the current page
 * This function runs in the content script context
 */
export const scrapePageContent = (): ScrapedData => {
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
    if (text && text.length < 500) { // Avoid very long blocks
      texts.push(text)
    }
  })

  // Extract all image sources
  const imgElements = document.querySelectorAll('img')
  imgElements.forEach((img) => {
    const src = img.src || img.getAttribute('data-src')
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

/**
 * Sends a message to the content script to scrape the page
 */
export const sendScrapeRequest = async (): Promise<ScrapedData> => {
  return new Promise((resolve, reject) => {
    chrome.tabs.query({ active: true, currentWindow: true }, (tabs) => {
      if (tabs[0].id === undefined) {
        reject(new Error('No active tab found'))
        return
      }

      chrome.tabs.sendMessage(
        tabs[0].id,
        { action: 'scrapePage' },
        (response) => {
          if (chrome.runtime.lastError) {
            reject(chrome.runtime.lastError)
          } else {
            resolve(response as ScrapedData)
          }
        }
      )
    })
  })
}
