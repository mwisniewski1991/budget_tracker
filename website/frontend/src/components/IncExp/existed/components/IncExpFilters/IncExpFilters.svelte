<script>
    import { incExpFilterLimitValue } from "../../../../store";

    let incExpFilterLimitUserInput;

    function onLimitChange(incExpFilterLimitUserInput){
        incExpFilterLimitValue.set(incExpFilterLimitUserInput);
    } 

</script>

<div class="container">
    <label for="owner_id" class="form-label">Ilośc rekordów</label>
    <select 
        class="form-select" 
        aria-label="Default select example" 
        id="incExpFilterLimit" 
        name="incExpFilterLimit" 
        bind:value={incExpFilterLimitUserInput} 
        on:change={onLimitChange(incExpFilterLimitUserInput)}>
    
    <option value="300">300</option>
    <option value="200">200</option>
    <option value="100">100</option>
    <option value="50" selected >50</option>
    <option value="10">10</option>
</div>