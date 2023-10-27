import React, { useState, useEffect } from 'react';
import { AlgorandClient } from '@algorand/algorand-sdk';

const funding = () => {

    const [fundingPoolAmount, setFundingPoolAmount] = useState(0);

    useEffect(() => {
        // Get the current funding pool amount from the blockchain
        const getFundingPoolAmount = async () => {
            const client = new AlgorandClient();
            const fundingPool = await client.getApplicationState(appId).getGlobalState(key: Bytes('funding_pool'));
            setFundingPoolAmount(fundingPool.value);
        };

        getFundingPoolAmount();
    }, []);

    const handleContribute = async () => {
        // Create a transaction to contribute to the funding pool
        const transaction = await client.contributeToFundingPool(appId, amount);

        // Sign the transaction
        const signedTransaction = await client.signTransaction(transaction);

        // Send the transaction to the blockchain
        await client.sendTransaction(signedTransaction);
    };

    return (
        <div>
            <h1>Funding Pool</h1>
            <p>Current funding pool amount: {fundingPoolAmount} ALGO</p>
            <button onClick={handleContribute}>Contribute to Funding Pool</button>
        </div>
    );
};

export default funding;