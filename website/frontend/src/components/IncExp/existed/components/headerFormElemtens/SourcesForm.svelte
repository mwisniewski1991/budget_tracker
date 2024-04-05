<script>
    export let isModifyMode;
    export let source;

    let sourcesPromise = getSources();

    async function getSources(){
        const resposne = await fetch('/api/v1/sources');
        const sources =  await resposne.json();
        return sources
    };

</script>

{#if isModifyMode}
    <input type="text" list="sources" class="form-control" id=source name=source placeholder="Źródło" bind:value={source}>
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
{:else}
    {#if source === ""}
        <span> - - - - </span>
    {:else}
        <span>{source}</span>
    {/if}

{/if}
