<script>
    import { userTypeId  } from '../store.js';

    let userType;

    function onTypeChange(){
        userTypeId.set(userType)
    };
  

</script>


<div class="formHeader">
    <div class="mb-3">
        <label for="date" class="form-label">Data</label>
        <input type="date" class="form-control" id="date" name="date">
    </div>
    
    <div class="mb-3">
        <label for="type_id" class="form-label">Rodzaj</label>
        <select class="form-select" aria-label="Default select example" id="type_id" name="type_id" bind:value={userType} on:change={onTypeChange}>

            <option value="1">Dochód</option>
            <option value="2">Wydatek</option>

        </select>
    </div>    

</div>

      