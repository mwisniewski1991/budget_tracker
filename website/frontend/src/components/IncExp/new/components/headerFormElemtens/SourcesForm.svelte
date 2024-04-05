<script>
    let sourcesPromise = getSources();

    async function getSources(){
        const resposne = await fetch('/api/v1/sources');
        const sources =  await resposne.json();
        return sources
    };

</script>


<input type="text" list="sources" class="form-control" id=source name=source placeholder="Źródło">
<datalist id="sources">
    {#await sourcesPromise}
        <p></p>
    {:then sourcesList} 
            {#each sourcesList as source}
            <option value={source.source_name}>
            {/each}
        {:catch Error}
            <p>Something went wrong</p>
    {/await}
</datalist>
