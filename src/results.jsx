import React, { useState, useEffect } from 'react';
import { AlgorandClient } from '@algorand/algorand-sdk';

const VotingResultsComponent = () => {

    const [results, setResults] = useState([]);

    useEffect(() => {
        // Get the voting results from the blockchain
        const getVotingResults = async () => {
            const client = new AlgorandClient();
            const results = await client.getQuadraticFundingResults(appId);
            setResults(results);
        };

        getVotingResults();
    }, []);

    return (
        <div>
            <h1>Voting Results</h1>
            <ul>
                {results.map((result) => (
                    <li key={result.projectId}>
                        {result.projectName}: {result.fundingAmount} ALGO
                    </li>
                ))}
            </ul>
        </div>
    );
};

export default VotingResultsComponent;