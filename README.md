# Picture_Perfect
Employing Data Abstractions in Image Search

## Background/Problem

- Identifying and retrieving similar images within large databases is computationally intensive
- 32-bit Color Images 
    - Each pixel is represented by three bytes (RGB)
    - Up to 256 possibly values per color channel (16,777,216 possible combinations)
    - Fourth byte is alpha channel depicting transparency
- Image pixel-map contain a lot of noise (e.g. elements in background of image) that make it hard to identify similar elements found in other photos

## Solution

- Performing data abstractions on images over distributed network decreases the complexity of the search space and only essential elements are compared for similarity

- Distributed networks allow the computational work to be split up between nodes to improve the overall speed of the image search



## Tech Stack

- **S3:** Storage
- **Apache Spark:** Distributed Cluster-Computing Framework 
- **PostgreSQL:** Queryable Relational Database

## Data Engineering Challenge

- Scaling up to full-scale dataset
- Optimization
    - Performing correct data abstractions so that a similarity comparison can be run efficiently across all images in dataset
- Partitioning dataset properly so all images are compared

## Business/Use Case
- Image search/retrieval (finds similar images)
- Quickly finding unwanted duplicates in image databases to save on storage space
- Security/Forensics: Narrowing down list of suspects using face, thumbprint, etc
- Online shopping search tool: find other products that look similar to the particular product you are interested in (e.g. similar style hats or shoes)


## Technologies
`Apache Spark`, `AWS S3`, `PostgreSQL`

## Presentation Link
http://bit.ly/Vasco_PicturePerfect
