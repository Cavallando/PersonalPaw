# Personal Paw
## Inspiration
Our project is based on the idea that Penn State is one of the largest undergraduate populations in the world, with **over 1000** clubs/organizations. We came to the realization that there are far too many oppurtunities for one student to get the chance to experience throughout his/her 4 short years at this University. 

Our group is working on a project separate to this one to aid in broadening a students perspective and enhancing his/her college experience to ultimately maximize his/her potential. Through machine learning and artificial intelligence our CAPSTONE project will learn how the student learns and offer events around campus, career paths, courses, social events, etc. 

We saw that this speech recognition platform would be a perfect module to build in conjunction with out app. 

This is Personal Paw.

## What it does
Personal Paw uses the Google API, DialogFlow, to read user made search requests and pull various data from many of Penn State's website. Personal Paw offers a fluid, user-friendly design to receive fast answers that usually require some digging.

## How we built it
At its core, Personal Paw is built using React.JS. This sleek front end design allows for a simple, yet efficient user experience. Our Front End makes POST requests to Google's DialogFlow API which in turn triggers our webhook, developed with Python in conjunction with the Flask microframework.

## Challenges we ran into
We realized early on that a user can type anything into this search and creating every possible conversation, fallback response for this application was a very daunting task. Since Penn State's resources are spread out over hundreds of webpages, each one requires custom querying/webscraping which held up development at times. In addition, we needed a custom fluent design that worked well with a not so custom API.

## Accomplishments that we're proud of
We are extremely proud of the build that we have as it serves as a proof of concept that this is 100% possible and useful. We also were proud of our ability to work efficiently as a team while continuing to express our passion for Software Development. 

## What we learned
Over the past 30 hours, we learned several new API's, debugging techniques, and that we hate webscraping. We also learned that Penn State's resources are widely spread out, which is understandable considering various web applications technical needs. Above all, this was a great reminder that we love what we do, especially when it helps our peers and betters our community. 

## What's next for Personal Paw
As mentioned before, we plan to implement this module in our overall application as well as continue to improve on it. We have also recognized that creating a Boilerplate template of this application so other students around the country could use it too would overall help us receive feedback as well as promote the open-ource community. Finally, we hope in the future to work with Penn State to continue development of Personal Paw and similar applications to promote student driven work.
