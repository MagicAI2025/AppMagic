import React from 'react';

const features = [
  {
    icon: '🪄',
    title: 'Instant App Creation',
    description: 'Generate complete applications in seconds, saving up to 90% development time',
    highlight: '90% faster development'
  },
  {
    icon: '🎯',
    title: 'Natural Language to Code',
    description: 'Simply describe your app in plain English, and watch it come to life',
    highlight: 'No coding required'
  },
  {
    icon: '🔄',
    title: 'Continuous Evolution',
    description: 'Your application evolves automatically, adapting to new requirements seamlessly',
    highlight: 'Self-evolving apps'
  },
  {
    icon: '👥',
    title: 'Team Efficiency',
    description: 'Boost your team productivity by 300% with AI-powered collaboration tools',
    highlight: '300% productivity boost'
  },
  {
    icon: '💡',
    title: 'Smart Suggestions',
    description: 'Accelerate development with intelligent code suggestions and optimizations',
    highlight: 'AI-powered insights'
  },
  {
    icon: '🛡️',
    title: 'Enterprise Ready',
    description: 'Deploy with confidence using enterprise-grade security and scalability',
    highlight: 'Production ready'
  },
  {
    icon: '📊',
    title: 'Visual Management',
    description: 'Manage your projects effortlessly with intuitive visual tools',
    highlight: 'Intuitive control'
  },
  {
    icon: '🔍',
    title: 'Code Quality Assurance',
    description: 'Ensure high-quality code with automated reviews and best practices',
    highlight: 'Quality guaranteed'
  },
  {
    icon: '🚀',
    title: 'Quick Deployment',
    description: 'Go from idea to production in minutes with one-click deployment',
    highlight: 'Instant deployment'
  }
];

const Features: React.FC = () => {
  return (
    <section className="py-20 bg-gradient-to-b from-gray-50 to-white">
      <div className="container mx-auto px-4">
        <h2 className="text-4xl font-bold text-center mb-12">
          Transform Your Ideas Into Reality
        </h2>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
          {features.map((feature, index) => (
            <div
              key={index}
              className="p-6 bg-white rounded-xl shadow-lg hover:shadow-xl transition-shadow duration-300"
            >
              <div className="text-4xl mb-4">{feature.icon}</div>
              <h3 className="text-xl font-semibold mb-2">{feature.title}</h3>
              <p className="text-gray-600 mb-4">{feature.description}</p>
              <span className="inline-block bg-blue-100 text-blue-800 text-sm font-semibold px-3 py-1 rounded-full">
                {feature.highlight}
              </span>
            </div>
          ))}
        </div>
      </div>
    </section>
  );
};

export default Features; 