import { scholarAdditions } from './scholar-additions';
import imageRecords from './publication-images.json';
import dateRecords from './publication-dates.json';

export interface PublicationImage {
  src: string;
  alt: string;
  caption: string;
  source: string;
  assetSource: string;
  width: number;
  height: number;
  kind: 'figure' | 'cover';
  thumbnail?: { src: string; alt: string; width: number; height: number };
}

export interface Publication {
  slug: string;
  title: string;
  shortTitle: string;
  year: number;
  publishedAt: string;
  venue: string;
  venueShort: string;
  authors: string[];
  equalContribution?: string[];
  topics: string[];
  summary: string;
  question: string;
  approach: string;
  links: { label: string; href: string }[];
  bibtex: string;
  featured: boolean;
  diagram?: 'repo' | 'escape' | 'proactive' | 'context';
  kind?: 'conference' | 'preprint' | 'technical-report' | 'project-report';
  statusLabel?: string;
  aliases?: string[];
  scholarIds?: string[];
  authorshipNote?: string;
  image?: PublicationImage;
}

export type PublicationRecord = Omit<Publication, 'publishedAt'>;

// Bibliographic metadata follows the ACL Anthology and ICLR proceedings.
// The descriptions below are short editorial summaries, rather than abstracts.
const originalPublications: PublicationRecord[] = [
  {
    slug: 'repoagent',
    title: 'RepoAgent: An LLM-Powered Open-Source Framework for Repository-level Code Documentation Generation',
    shortTitle: 'RepoAgent',
    year: 2024,
    venue: 'EMNLP 2024 · System Demonstrations',
    venueShort: 'EMNLP 2024',
    authors: ['Qinyu Luo', 'Yining Ye', 'Shihao Liang', 'Zhong Zhang', 'Yujia Qin', 'Yaxi Lu', 'Yesai Wu', 'Xin Cong', 'Yankai Lin', 'Yingli Zhang', 'Xiaoyin Che', 'Zhiyuan Liu', 'Maosong Sun'],
    equalContribution: ['Qinyu Luo', 'Yining Ye'],
    topics: ['Code intelligence', 'Agent systems'],
    summary: 'An open-source agent that generates and maintains documentation with a view of the whole code repository.',
    question: 'How can documentation stay useful as a repository grows and its code changes?',
    approach: 'RepoAgent uses language models to generate repository-level documentation and update it alongside code changes. The framework connects documentation generation with repository understanding, supporting an ongoing development workflow.',
    links: [
      { label: 'Paper', href: 'https://aclanthology.org/2024.emnlp-demo.46/' },
      { label: 'PDF', href: 'https://aclanthology.org/2024.emnlp-demo.46.pdf' },
      { label: 'Code', href: 'https://github.com/OpenBMB/RepoAgent' },
    ],
    bibtex: `@inproceedings{luo-etal-2024-repoagent,
    title = "{R}epo{A}gent: An {LLM}-Powered Open-Source Framework for Repository-level Code Documentation Generation",
    author = "Luo, Qinyu  and
      Ye, Yining  and
      Liang, Shihao  and
      Zhang, Zhong  and
      Qin, Yujia  and
      Lu, Yaxi  and
      Wu, Yesai  and
      Cong, Xin  and
      Lin, Yankai  and
      Zhang, Yingli  and
      Che, Xiaoyin  and
      Liu, Zhiyuan  and
      Sun, Maosong",
    editor = "Hernandez Farias, Delia Irazu  and
      Hope, Tom  and
      Li, Manling",
    booktitle = "Proceedings of the 2024 Conference on Empirical Methods in Natural Language Processing: System Demonstrations",
    month = nov,
    year = "2024",
    address = "Miami, Florida, USA",
    publisher = "Association for Computational Linguistics",
    url = "https://aclanthology.org/2024.emnlp-demo.46/",
    doi = "10.18653/v1/2024.emnlp-demo.46",
    pages = "436--464"
}`,
    featured: true,
    diagram: 'repo',
  },
  {
    slug: 'proactive-agent',
    title: 'Proactive Agent: Shifting LLM Agents from Reactive Responses to Active Assistance',
    shortTitle: 'Proactive Agent',
    year: 2025,
    venue: 'International Conference on Learning Representations 2025',
    venueShort: 'ICLR 2025',
    authors: ['Yaxi Lu', 'Shenzhi Yang', 'Cheng Qian', 'Guirong Chen', 'Qinyu Luo', 'Yesai Wu', 'Huadong Wang', 'Xin Cong', 'Zhong Zhang', 'Yankai Lin', 'Weiwen Liu', 'Yasheng Wang', 'Zhiyuan Liu', 'Fangming Liu', 'Maosong Sun'],
    topics: ['Proactive assistance', 'Agent systems'],
    summary: 'Learning when an agent should offer help, using observations of user activity and feedback on proposed tasks.',
    question: 'Can an agent recognize a useful next step before the user explicitly asks for help?',
    approach: 'The work combines activity-based task prediction, human acceptance labels, a learned evaluator, and the ProactiveBench data pipeline. Fine-tuning studies examine how these signals help agents decide when and how to offer assistance.',
    links: [
      { label: 'Paper', href: 'https://proceedings.iclr.cc/paper_files/paper/2025/hash/75c37811e830bf029584b1c6fac17726-Abstract-Conference.html' },
      { label: 'OpenReview', href: 'https://openreview.net/forum?id=sRIU6k2TcU' },
      { label: 'arXiv', href: 'https://arxiv.org/abs/2410.12361' },
      { label: 'Code & data', href: 'https://github.com/thunlp/ProactiveAgent' },
    ],
    bibtex: `@inproceedings{ICLR2025_75c37811,
 author = {Lu, Yaxi and Yang, Shenzhi and Qian, Cheng and Chen, Guirong and Luo, Qinyu and Wu, Yesai and Wang, Huadong and Cong, Xin and Zhang, Zhong and Lin, Yankai and Liu, Weiwen and Wang, Yasheng and Liu, Zhiyuan and Liu, Fangming and Sun, Maosong},
 booktitle = {International Conference on Learning Representations},
 editor = {Y. Yue and A. Garg and N. Peng and F. Sha and R. Yu},
 pages = {47431--47457},
 title = {Proactive Agent: Shifting LLM Agents from Reactive Responses to Active Assistance},
 url = {https://proceedings.iclr.cc/paper_files/paper/2025/file/75c37811e830bf029584b1c6fac17726-Paper-Conference.pdf},
 volume = {2025},
 year = {2025}
}`,
    featured: true,
    diagram: 'proactive',
  },
  {
    slug: 'escapebench',
    title: 'EscapeBench: Towards Advancing Creative Intelligence of Language Model Agents',
    shortTitle: 'EscapeBench',
    year: 2025,
    venue: 'ACL 2025 · Main Conference',
    venueShort: 'ACL 2025',
    authors: ['Cheng Qian', 'Peixuan Han', 'Qinyu Luo', 'Bingxiang He', 'Xiusi Chen', 'Yuji Zhang', 'Hongyi Du', 'Jiarui Yao', 'Xiaocheng Yang', 'Denghui Zhang', 'Yunzhu Li', 'Heng Ji'],
    topics: ['Creative reasoning', 'Agent evaluation'],
    summary: 'Room-escape environments for studying creative problem-solving, implicit goals, and unexpected uses of familiar tools.',
    question: 'How do agents solve unfamiliar problems when neither the goal nor the right tool use is obvious?',
    approach: 'EscapeBench places agents in interactive room-escape games. EscapeAgent adds foresight for exploring possible tool uses and reflection for revisiting unresolved tasks, making creative adaptation part of the agent loop.',
    links: [
      { label: 'Paper', href: 'https://aclanthology.org/2025.acl-long.39/' },
      { label: 'PDF', href: 'https://aclanthology.org/2025.acl-long.39.pdf' },
      { label: 'Code & data', href: 'https://github.com/qiancheng0/EscapeBench' },
    ],
    bibtex: `@inproceedings{qian-etal-2025-escapebench,
    title = "{E}scape{B}ench: Towards Advancing Creative Intelligence of Language Model Agents",
    author = "Qian, Cheng  and
      Han, Peixuan  and
      Luo, Qinyu  and
      He, Bingxiang  and
      Chen, Xiusi  and
      Zhang, Yuji  and
      Du, Hongyi  and
      Yao, Jiarui  and
      Yang, Xiaocheng  and
      Zhang, Denghui  and
      Li, Yunzhu  and
      Ji, Heng",
    editor = "Che, Wanxiang  and
      Nabende, Joyce  and
      Shutova, Ekaterina  and
      Pilehvar, Mohammad Taher",
    booktitle = "Proceedings of the 63rd Annual Meeting of the Association for Computational Linguistics (Volume 1: Long Papers)",
    month = jul,
    year = "2025",
    address = "Vienna, Austria",
    publisher = "Association for Computational Linguistics",
    url = "https://aclanthology.org/2025.acl-long.39/",
    doi = "10.18653/v1/2025.acl-long.39",
    pages = "798--820",
    ISBN = "979-8-89176-251-0"
}`,
    featured: true,
    diagram: 'escape',
  },
  {
    slug: 'long-context-bias',
    title: 'Distance between Relevant Information Pieces Causes Bias in Long-Context LLMs',
    shortTitle: 'Long-context positional bias',
    year: 2025,
    venue: 'Findings of the Association for Computational Linguistics: ACL 2025',
    venueShort: 'Findings of ACL 2025',
    authors: ['Runchu Tian', 'Yanghao Li', 'Yuepeng Fu', 'Siyang Deng', 'Qinyu Luo', 'Cheng Qian', 'Shuo Wang', 'Xin Cong', 'Zhong Zhang', 'Yesai Wu', 'Yankai Lin', 'Huadong Wang', 'Xiaojiang Liu'],
    equalContribution: ['Runchu Tian', 'Yanghao Li'],
    topics: ['Long context', 'Model evaluation'],
    summary: 'Studying how the spacing between related facts changes a language model’s ability to use a long context.',
    question: 'Does the distance between relevant facts matter, beyond their individual positions in a long input?',
    approach: 'LongPiBench varies the placement and spacing of multiple relevant information pieces across tasks and input lengths. The study distinguishes absolute position from relative distance to reveal biases that single-fact retrieval tests can miss.',
    links: [
      { label: 'Paper', href: 'https://aclanthology.org/2025.findings-acl.28/' },
      { label: 'PDF', href: 'https://aclanthology.org/2025.findings-acl.28.pdf' },
      { label: 'Code & data', href: 'https://github.com/thunlp/LongPiBench' },
    ],
    bibtex: `@inproceedings{tian-etal-2025-distance,
    title = "Distance between Relevant Information Pieces Causes Bias in Long-Context {LLM}s",
    author = "Tian, Runchu  and
      Li, Yanghao  and
      Fu, Yuepeng  and
      Deng, Siyang  and
      Luo, Qinyu  and
      Qian, Cheng  and
      Wang, Shuo  and
      Cong, Xin  and
      Zhang, Zhong  and
      Wu, Yesai  and
      Lin, Yankai  and
      Wang, Huadong  and
      Liu, Xiaojiang",
    editor = "Che, Wanxiang  and
      Nabende, Joyce  and
      Shutova, Ekaterina  and
      Pilehvar, Mohammad Taher",
    booktitle = "Findings of the {A}ssociation for {C}omputational {L}inguistics: {ACL} 2025",
    month = jul,
    year = "2025",
    address = "Vienna, Austria",
    publisher = "Association for Computational Linguistics",
    url = "https://aclanthology.org/2025.findings-acl.28/",
    doi = "10.18653/v1/2025.findings-acl.28",
    pages = "521--533",
    ISBN = "979-8-89176-256-5"
}`,
    featured: false,
    diagram: 'context',
  },
];

const originalScholarIds: Record<string, string[]> = {
  repoagent: ['JoZmwDi-zQgC', 'WqliGbK-hY8C'],
  'proactive-agent': ['dTyEYWd-f8wC'],
  escapebench: ['SdhP9T11ey4C', 'eq2jaN3J8jMC'],
  'long-context-bias': ['9vf0nzSNQJEC'],
};
const images = imageRecords as Record<string, PublicationImage>;
const dates = dateRecords as Record<string, { month: string; basis: string; sources: string[] }>;

export const publications: Publication[] = [...originalPublications, ...scholarAdditions].map(publication => {
  const image = images[publication.slug];
  if (!image) throw new Error(`Missing original figure or cover for ${publication.slug}`);
  const publishedAt = dates[publication.slug]?.month;
  if (!publishedAt || !/^\d{4}-(0[1-9]|1[0-2])$/.test(publishedAt) || Number(publishedAt.slice(0, 4)) !== publication.year) {
    throw new Error(`Missing or inconsistent publication month for ${publication.slug}`);
  }
  return {
    kind: 'conference',
    ...publication,
    publishedAt,
    scholarIds: publication.scholarIds || originalScholarIds[publication.slug] || [],
    aliases: publication.slug === 'escapebench'
      ? ['EscapeBench: Pushing Language Models to Think Outside the Box']
      : publication.aliases,
    image,
  };
});

// Keep the requested Seed reports first; order all other work by publication month.
const displayPriority: Record<string, number> = { 'seed-2-1': 2, 'seed-2-0': 1 };
export const displayPublications = [...publications].sort((a, b) =>
  (displayPriority[b.slug] ?? 0) - (displayPriority[a.slug] ?? 0) || b.publishedAt.localeCompare(a.publishedAt)
);
