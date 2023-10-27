import React, { useState, useEffect } from 'react';
import { AlgorandClient } from '@algorand/algorand-sdk';

const ProjectsComponent = () => {

    const [projects, setProjects] = useState([]);

    useEffect(() => {
        // Get a list of all projects from the blockchain
        const getProjects = async () => {
            const client = new AlgorandClient();
            const projects = await client.getQuadraticFundingProjects(appId);
            setProjects(projects);
        };

        getProjects();
    }, []);

    const handleVote = async (projectId) => {
        // Create a transaction to vote on the project
        const transaction = await client.voteOnProject(appId, projectId);

        // Sign the transaction
        const signedTransaction = await client.signTransaction(transaction);

        // Send the transaction to the blockchain
        await client.sendTransaction(signedTransaction);
    };

    return (
        <div>
            <h1>Projects</h1>
            <ul>
                {projects.map((project) => (
                    <li key={project.id}>
                        {project.name}
                        <button onClick={() => handleVote(project.id)}>Vote</button>
                    </li>
                ))}
            </ul>
        </div>
    );
};

export default ProjectsComponent;