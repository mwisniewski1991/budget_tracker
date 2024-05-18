<script>
    export let componentSourceFilter = "";
</script>

<div>
    <label for="incExpFilterSource" class="form-label">Źródło</label>
    <input type="text" class="form-control" id="incExpFilterSource" bind:value={componentSourceFilter}>
</div>