# Job Description QCM Generator Using LLMs

This project generates advanced multiple-choice (QCM) questions based on job descriptions using large language models (LLMs). The goal is to create high-quality questions that assess candidates' skills and competencies relevant to the job.

## Part of a Larger Recruitment Service

This QCM generator is a service within a broader AI-powered recruitment platform. The platform leverages LLMs to streamline various aspects of the recruitment process, from evaluating candidates' skills based on job descriptions to sorting candidates by their test scores and sending interview invitations. This tool specifically focuses on generating skill-based questions to ensure accurate candidate assessment.

## Features

- **Automated question generation**: Generates QCM questions directly from job descriptions.
- **Skill-based assessment**: Questions are designed to evaluate the candidate's skills and knowledge in areas directly relevant to the job.
- **JSON output**: The questions and answers are provided in a structured JSON format, making integration easy.

## Example Output

```json
{
  "questions": [
    {
      "question": "What is the most efficient way to improve database performance in a large-scale web application?",
      "options": ["Indexing", "More RAM", "Denormalization", "Caching"],
      "answer": "Indexing"
    },
    {
      "question": "Which JavaScript framework is best suited for building scalable front-end applications?",
      "options": ["React", "jQuery", "Backbone.js", "Ember.js"],
      "answer": "React"
    }
  ]
}
