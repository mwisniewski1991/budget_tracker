<script>
    import { incExpFilterDetailsVisible } from "../../../../../store";

    let detailsVisibleUserInput;

    function onDetailsVisibleChange(userInput){
        if(userInput === "true"){
            incExpFilterDetailsVisible.set(true);
            localStorage.setItem("incExpFilterDetailsVisibleLocalData", true);
        };
        if(userInput === "false"){
            incExpFilterDetailsVisible.set(false);
            localStorage.setItem("incExpFilterDetailsVisibleLocalData", false);
        };
    } 

</script>

<div>
    <label for="owner_id" class="form-label">Szczegóły</label>
    <select 
        class="form-select" 
        id="incExpDetailVisible" 
        name="incExpDetailVisible" 
        bind:value={detailsVisibleUserInput} 
        on:change={onDetailsVisibleChange(detailsVisibleUserInput)}>
    
    {#if $incExpFilterDetailsVisible === true}
        <option value="true" selected>Widoczne</option>
        <option value="false"        >Ukryte</option>
    {:else}
        <option value="true"          >Widoczne</option>
        <option value="false" selected>Ukryte</option>
    {/if}
    </select>
</div>