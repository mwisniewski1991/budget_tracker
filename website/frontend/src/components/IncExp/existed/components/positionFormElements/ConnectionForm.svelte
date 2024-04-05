<script>
    export let isModifyMode;
    export let positionId;
    export let connection;

    let htmlNamePosition = `connection_${positionId}`;

</script>

{#if isModifyMode}
    {#if connection}
        <input type="text" class="form-control" id={htmlNamePosition} name={htmlNamePosition} value={connection}>
    {:else}
        <input type="text" class="form-control" id={htmlNamePosition} name={htmlNamePosition} placeholder="Powiązanie">
    {/if}
{:else}
    {#if connection === ""}
        <span> - - - - </span>
    {:else}
        <span>{connection}</span>
    {/if}

{/if}