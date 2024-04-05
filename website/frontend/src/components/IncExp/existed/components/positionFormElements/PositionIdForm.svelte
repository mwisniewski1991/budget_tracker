<script>
    export let positionId;
    let htmlNamePosition = `position_id_${positionId}`;
    
</script>

<input 
    type="hidden" 
    class="form-control" 
    id={htmlNamePosition} 
    name={htmlNamePosition} 
    value={positionId}>