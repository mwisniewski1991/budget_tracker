<script>
    export let isModifyMode;
    export let positionId;
    export let comment;

    let htmlNamePosition = `comment_${positionId}`;

</script>

{#if isModifyMode}
    {#if comment}
        <input type="text" class="form-control" id={htmlNamePosition} name={htmlNamePosition} value={comment}>
    {:else}
        <input type="text" class="form-control" id={htmlNamePosition} name={htmlNamePosition} placeholder="Komentarz">
    {/if}
{:else}
    {#if comment === ""}
        <span> - - - - </span>
    {:else}
        <span>{comment}</span>
    {/if}
{/if}