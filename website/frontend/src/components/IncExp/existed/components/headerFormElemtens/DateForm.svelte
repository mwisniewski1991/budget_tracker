<script>
    export let isModifyMode;
    export let header_date;
</script>

{#if isModifyMode}
    <input type="date" class="form-control" id="date" name="date" bind:value={header_date}>
{:else}
    <span>{header_date}</span>
{/if}
