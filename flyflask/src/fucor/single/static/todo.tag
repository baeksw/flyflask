<todo>
<!-- 
<blockquote>
  <p>할일 목록</p>
  <footer>Someone famous in <cite title="Source Title">Source Title</cite></footer>
</blockquote>
 -->

<div class="panel panel-primary">
	<div class="panel-heading">{ opts.title }<span class="pull-right"><button class="btn btn-info btn-xs" onclick={update_all}>SAVE</button></span></div>
	<div class="panel-body">
		<ul class="list-unstyled">
			<li each={items.filter(whatShow)}>
					<div class="checkbox">
      <label class={ completed: done }>
        <input type="checkbox" checked={ done } onclick={ parent.toggle }> { title }
        </div>
      </label>
    </li>
		</ul>
		<form onsubmit={add}>
			<div class="row">
				<div class="col-md-8">
						<input class="form-control input-sm" ref="input" onkeyup={edit }>
				</div>
				<div class="col-md-4">
					<button class="btn btn-primary btn-sm" disabled={!text }>Add #{ items.filter(whatShow).length + 1 }</button>
					<button class="btn btn-primary btn-sm" type="button" disabled={
						items.filter(onlyDone).length== 0 } onclick={removeAllDone }>
						X{ items.filter(onlyDone).length }</button>
				</div>
			</div>
		</form>
	</div>
</div>

<!-- this script tag is optional -->
  <script>

	
    this.items = opts.items
    
    edit(e) {
      this.text = e.target.value
    }

    add(e) {
      if (this.text) {
        this.items.push({ title: this.text })
        this.text = this.refs.input.value = ''
      }
      e.preventDefault()
    }
    
    update_all(e) {
        if (this.text) {
          this.items.push({ title: this.text })
          this.text = this.refs.input.value = ''
        }

        console.log('update!!'+JSON.stringify(opts));
        var param = { 'data' : opts };
 		var _ajax = $.ajax({ url: '/todo' , data:JSON.stringify(param) , type:'POST' ,dataType : 'json' });
 		_ajax.done(function(d){
 			console.log("<done>")
 			console.log(d)
 			console.log("<done>")
 		})
        
        //this.postJSON('/todo',opts).success(function(data){ alert('success!!') });
 		/*
        postJSON('/todo',opts) .done(function(data){ alert('success!!') })
        	.fail(function(response, status){ console.log("[fail] response=>"+status) }) .always(function(){ console.log('job done.') });
        */
        
        e.preventDefault()
      }

    removeAllDone(e) {
      this.items = this.items.filter(function(item) {
        return !item.done
      })
    }

    // an two example how to filter items on the list
    whatShow(item) {
      return !item.hidden
    }

    onlyDone(item) {
      return item.done
    }

    toggle(e) {
      var item = e.item
      item.done = !item.done
      return true
    }
  </script>

</todo>