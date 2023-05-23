---
layout: archive
# title: "CV"
permalink: /cv/
author_profile: true
redirect_from:
  - /resume
---

{% include base_path %}

## Education

### Hohai University, School of Computer Science and Information | **China | 2019.09 – 2023.06**


Main Courses: 
- Artificial Intelligence
- Operating Systems
- Data Structures
- Algorithm Design
- Database Systems.

---

### University of Delaware, Department of Computer and Information Sciences ｜ **USA | 2022.07 - 2022.11**

Summer Research intern
Advisor: Professor Weisong Shi


# Work Experience
------
- Intelligent Stethoscope for Heart Sound Recognition | Founder | FinzHealth IoT Technology | 2021.05 - Present
  - Invented a wireless intelligent stethoscope during the COVID-19 pandemic and founded FinzHealth IoT Technology Co., LTD; established the first Chinese database for heart sounds from patients with corona virus.
  - Obtained three patents by designing the hardware structure of the product, raised a million yuan in financing and reached hundreds of test users with our minimum viable product.
  - Filtered the data to reduce high-frequency noise, downsampled to increase the sensing field and normalized the audio signal to unify the audio scale.
  - Extracted features by using spectral analysis and trained neural network models to classify four heart maladies, achieving a 97% accuracy on the test dataset.

- Research and application of large-scale language models in the financial field | Internship
  - China International Capital Corporation Limited (CICC) | AI Group | 2022.07 - Present
  - Investigated the application of large language models and ran some open-source models such as CPM-Ant, GPT, and flan-T5 to evaluate their effects in text generation and question answering.
  - Contributed a dataset called PsQScore by crawling data from Bing.com, perplexity.ai and ChatGPT, combining with washed data from the DuReader and T2Ranking dataset.
  - Fintuned a model with the capability of generating search results with citations using the self-constructed data. Then I combined it with the company's internal database and use it in the search and investment research report generation functions in financial field.

# Research Experience
------
- Self-Driving Task Scheduling Framework based on Docker and Edge Computing | 2022.07 - Present
  - Advisor: Professor Weisong Shi | Chair of Computer Science Department | University of Delaware | USA
  - Devised a task scheduling framework to solve the autonomous driving task scheduling problem on software-defined vehicles, encapsulating four algorithms and deployed on docker to create an experimental environment.
  - Combined reinforcement learning with a dual-timescale mechanism, using actor-critic algorithm to automatically learn scheduling strategies for driving tasks.
  - Proposed a dynamic change formula based on image similarity for large time scale, optimizing orchestrating overhead assembling a matrix-like service relevance coefficient update mechanism to accelerate model learning--these innovations helped improve the framework throughput rate by 12.04% and stability (using the variance of the throughput rate) by 3.56%.
  - Designed a global feature-fusion method to generate the state of reinforcement learning, and, eventually, the throughput rate was increased from 50% to 79% ~ 97%, and the stability was increased by 48.68%.

- Image Style Transfer based on VGG19 Pre-trained Model | 2022.03 - 2022.05
  - Advisor: Dr. Evelyn | Stanford University | USA
  - Built a multilayer convolutional neural network using VGG19 Pre-trained Model and yielded 763 image style-transfer pairs of different sizes and themes in order to imitate human painting styles.
  - Discovered the correspondence between image structure pattern and style similarity, proposed an improved method of fusing object recognition and style transfer with clearer line texture and better color block separation.

# Projects
------
- Cooperative Control System for UAV Swarms based on Cloud-Side Collaboration | 2021.07 - 2021.09
  - Advisor: Yingchi Mao | Vice Dean of School of Computer Science | Hohai University | China
  - Implemented automate drone tasks including waypoint planning, timed photo-taking in UAV control system.
  - Adjusted the layout and structure of the mobile control system, optimized the UI interface, and implemented RTMP live streaming push to the edge server.

- Big Data Storage and Computing Separation System based on HUAWEI CLOUD | 2021.12 - 2022.02
  - Built a Hadoop cluster, configured environment variables and initialized the namenodes.
  - Stored the collected YouTube videos into the Hadoop Distributed File System of the Hadoop cluster, and used the MapReduce service to implement querying and sorting functions such as the number of plays and comments.

# AWARDS
------
- National Level:
  - Second inventor of three patents
  - Excellent completion of national innovation and entrepreneurship training project (first place)
  - First prize at the National University Art Exhibition in 2021

- Provincial Level:
  - Third Prize at the Jiangsu "Internet+" Innovation and Entrepreneurship Competition
  - Third Prize at the "Winning in Nanjing" Innovation and Entrepreneurship Competition

- School Level:
  - 2021 Science and Technology Innovation Scholarship (5%)
  - Academic Excellence Scholarship (5%)
  - 2021 Leader of Academic Style Construction (1%)
  - Second prize at the Web Design Competition (5%)

# ACTIVITIES
------
- Documentary Director | Producer | 2020.02 - 2020.08
  - Independently produced the documentary film "Honglin Cuo". It was shown by CCTV-10, with a total viewership of more than 77 million.
  - Filmed a documentary of Fujian medical team's fight against COVID-19 called "The March", which was reflected by numerous official media outlets, with more than 1 million pageviews.
  - Received a letter of thanks from the Affiliated Union Hospital of Fujian Medical University, and the work was included in the Digital Museum of Huazhong University of Science and Technology.

# SKILLS
------
- Programming Languages: C, Java, Python, JavaScript, HTML, SQL.
- Technologies: PyTorch, TensorFlow, Oracle Database, Spring Boot, Docker, Maven, GaussDB.

<!-- 
Publications
======
  <ul>{% for post in site.publications %}
    {% include archive-single-cv.html %}
  {% endfor %}</ul>
  
Talks
======
  <ul>{% for post in site.talks %}
    {% include archive-single-talk-cv.html %}
  {% endfor %}</ul>
  
Teaching
======
  <ul>{% for post in site.teaching %}
    {% include archive-single-cv.html %}
  {% endfor %}</ul>
  
Service and leadership
======
* Currently signed in to 43 different slack teams -->
