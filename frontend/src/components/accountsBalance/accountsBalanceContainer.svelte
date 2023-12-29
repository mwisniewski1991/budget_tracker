<script>

        let ownersAccountsAmountsPromise = getOwnersAccountsAmounts();

        async function getOwnersAccountsAmounts(){
                const resposne = await fetch('/api/v1/owners-accounts-amount');
                const results =  await resposne.json();
                return results
        };

</script>


<div class="container-sm">
        <div class="container">

                <div class="row">
                        <div class="col"><strong>Właściciel</strong></div>
                        <div class="col"><strong>Konto</strong></div>
                        <div class="col"><strong>Stan</strong></div>
                </div>

                {#await ownersAccountsAmountsPromise}
                        <p></p>
                {:then ownersAccountsAmountsList} 
                {#each ownersAccountsAmountsList as row }
                        <div class="row">
                                <div class="col">{row.owner}</div>
                                <div class="col">{row.account}</div>
                                <div class="col">{row.amount_sum}</div>
                        </div>
                {/each}
                {:catch Error}
                        <p>Something went wrong</p>
                {/await}
                
        </div>
</div>