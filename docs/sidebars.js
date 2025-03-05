// @ts-check

// This runs in Node.js - Don't use client-side code here (browser APIs, JSX...)

/**
 * Creating a sidebar enables you to:
 - create an ordered group of docs
 - render a sidebar for each doc of that group
 - provide next/previous navigation

 The sidebars can be generated from the filesystem, or explicitly defined here.

 Create as many sidebars as you want.

 @type {import('@docusaurus/plugin-content-docs').SidebarsConfig}
 */
const sidebars = {
  // By default, Docusaurus generates a sidebar from the docs folder structure
  // tutorialSidebar: [{type: 'autogenerated', dirName: '.'}],

  // But you can create a sidebar manually
  tutorialSidebar: [
    'intro',
    {
      type: 'category',
      label: 'Tutorials',
      link: {type: 'doc', id: 'tutorials/intro'},
      items: [
        // 'tutorials/roleplay-chatbot',
        'tutorials/customer-service',
        'tutorials/booking-service'
      ],
    },
    'Config',
    {
      type: 'category',
      label: 'Taskgraph',
      link: {type: 'doc', id: 'Taskgraph/intro'},
      items: [
        'Taskgraph/Generation'
      ],
    },
    'MessageState',
    {
      type: 'category',
      label: 'Workers',
      link: {type: 'doc', id: 'Workers/intro'},
      items: [
        'Workers/Workers',
        'Workers/MessageWorker',
        'Workers/RAGWorker',
        'Workers/DatabaseWorker',
        'Workers/SearchWorker',
        'Workers/DefaultWorker'
      ],
    },
    'Tools',
    {
      type: 'category',
      label: 'Integration',
      link: {type: 'doc', id: 'Integration/intro'},
      items: [
        'Integration/Hubspot'
      ],
    },
    {
      type: 'category',
      label: 'Evaluation',
      link: {type: 'doc', id: 'Evaluation/intro'},
      items: [
        'Evaluation/UserSimulator',
        'Evaluation/Metrics'
      ]
    }
  ],
};

export default sidebars;
