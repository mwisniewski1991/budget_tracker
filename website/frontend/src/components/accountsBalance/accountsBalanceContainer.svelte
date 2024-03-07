<script>
        import AcountsCard from "./acountsCard.svelte"; 

        let ownersAccountsAmountsPromise = getOwnersAccountsAmounts();

        async function getOwnersAccountsAmounts(){
                const resposne = await fetch('/api/v1/owners-accounts-amount');
                const results =  await resposne.json();
                return results
        };

</script>


<div class="container-sm">
        
        {#await ownersAccountsAmountsPromise}
        <p></p>
        {:then ownersAccountsAmountsList} 
        {#each ownersAccountsAmountsList as ownerRow }

                <div class="card-group">
                        {#each ownerRow.owner_accounts as owner_accounts }
                        <AcountsCard 
                                owner_id={ownerRow.owner_id} 
                                owner={ownerRow.owner} 
                                account={owner_accounts.account_name} 
                                amount={owner_accounts.amount_sum}
                                last_update={owner_accounts.last_update}        
                                ></AcountsCard>
                        {/each}
                </div>
        {/each}
        {:catch Error}
                <p>Something went wrong</p>

        {/await}
</div>