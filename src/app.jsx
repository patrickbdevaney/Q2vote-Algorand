import React from 'react';
import FundingPoolComponent from './FundingPoolComponent';
import ProjectsComponent from './ProjectsComponent';
import VotingResultsComponent from './VotingResultsComponent';

const App = () => {
  return (
    <div>
      <h1>Quadratic Funding App</h1>
      <FundingPoolComponent />
      <ProjectsComponent />
      <VotingResultsComponent />
    </div>
  );
};

export default App;