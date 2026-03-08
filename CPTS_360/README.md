# Crimson Code Reflection
## Activity Description
Our expectations coming into this hackathon were to learn how AI detection processes work, specifically how AI image detection works. Our motivation for this idea was that AI images are getting better and better over time, so we wanted a tool that can locate trends that AI generates and notify the user.

## Technical Decisions
The general pipeline for our project is that the web extension would scrape the webpage for all its images and text, and then send the text to a Hugging Face AI model we found that specializes in GPT & Gemini responses. As for the images, we first check the image metadata, if it shows AI sources, then we flag it as AI. Otherwise, we run it through the Sightengine API, which splits the image down into 16x16 pixel sections and then performs multiple matrix operations on the images to detect AI noise and unusual smoothness of edges, which would indicate that AI was used in the creation of the image.

## Contributions (Team)
I worked on the backend, mainly setting up all the API calls and agent setups, and also did the testing through FastAPI. I also researched and found the APIs and AIs to use.

## Quality Assessment
I would say that we did relatively well. I am proud to say that the extension works for both image and text detection. While we didn't win any category, I believe that the experience and knowledge that we gained in this hackathon were worth it.
