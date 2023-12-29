<script>
    import HeaderContainer from "./headerContainer.svelte";

    let headersPromise = getHeaders();

    async function getHeaders(){
        
        const resposne = await fetch('/api/v1/positions');
        const results =  await resposne.json();
        return results
    };


</script>

<div>
    {#await headersPromise}
        <p></p>
    {:then headersList} 
        {#each headersList as header }
            <HeaderContainer {...header}/>    
        {/each}
        {:catch Error}
            <p>Something went wrong</p>
    {/await}
</div>






