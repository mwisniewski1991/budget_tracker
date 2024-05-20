<script>
        import AcountsCard from "./acountsCard.svelte"; 

        let ownersAccountsAmountsPromise = getOwnersAccountsAmounts();

        async function getOwnersAccountsAmounts(){
                const resposne = await fetch('/api/v1/owners-accounts-amount');
                const results =  await resposne.json();
                console.log(results)
                return results
        };

</script>


<div class="container-sm">
        
        {#await ownersAccountsAmountsPromise}
        <p></p>
        {:then ownersAccountsAmountsList} 
        {#each ownersAccountsAmountsList as ownerRow }

                <div class="card-group">
                        {#each ownerRow.accounts as account }
                        <AcountsCard 
                                owner_id={ownerRow.owner_id} 
                                owner={ownerRow.owner_name} 
                                account={account.name} 
                                amount={account.amount_sum}
                                last_update={account.last_update}        
                                ></AcountsCard>
                        {/each}
                </div>
        {/each}
        {:catch Error}
                <p>Something went wrong</p>

        {/await}
</div>