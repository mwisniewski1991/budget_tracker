<script>
    export let owner_id;
    export let owner;
    export let account;
    export let amount;
    export let last_update;

    function colorForOwner(owner_obj){
        switch(owner_obj){
            case 1:
                return "bg-success"
            case 2:
                return "bg-danger"
            case 3:
                return "bg-warning"
            case 4:
                return "bg-info"
            default: 
                return "bg-secondary"
        }
    };

</script>


<div class="card {colorForOwner(owner_id)} mb-3" style="max-width: 18rem;">
    <div class="card-header">{owner}</div>
    <div class="card-body">
      <h5 class="card-title">{account}</h5>
      <p class="card-text"><small>{last_update}</small></p>
      <p class="card-text">{amount}</p>
    </div>
</div>