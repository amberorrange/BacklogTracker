"use strict";

const BacklogEntry = (props) => {
  return (
    
    <div className="row">
      <div className="col col-3 col-sm-9 offset-sm-2 col-md-4 col-lg-6  col-xl-6 col-xxl-8 offset-xxl-2 ">

        <div className="card card-style">

          <div className='row g-0'>

            <div className='col-3'>
              <img  className="img-fluid bl-entry-img rounded-start" src={props.image}/>
            </div>

            <div className='col'>
              <div className='card-body pt-0'>
              <h4 className="backlog-entry-title card-title">{props.title}</h4>

                <ul class="list-group list-group-horizontal">
                  <h6 className="card-subtitle right-border list-group-item">Genre:  <p>{props.genre}</p></h6>
                  <h6 className="card-subtitle right-border list-group-item">Ownership Status: {props.ownership_status}</h6>
                  <h6 className="card-subtitle right-border list-group-item">Play Status: {props.play_status ? 'Currently Playing' : 'Not Playing'}</h6>
                  <h6 className="card-subtitle list-group-item">Platform: {props.platform}</h6>
                </ul>


              </div>
            </div> 


          </div> 

        </div> 

      </div>
    </div>
  );
}

const FilterOption = ({ options, disabledLabel}) => {
  return (
    <React.Fragment>
       <option value="" defaultValue disabled>
        {disabledLabel}
      </option>
      <option value="All" key="All">All</option>
      {options.map((option) => (
        <option key={option} value={option}>{option}</option> 
      ))}
    </React.Fragment>
  )
}

const Select = (props) => {
  return (
    <div>
      <select  value={props.value} onChange={props.onchange} className='form-select form-select-sm'>
        <FilterOption
          disabledLabel=""
          options={props.options}
        />
      </select>
    </div>
  )
}

const FilterOptions = (props) => {
  return (
    <div> 
      <Select 
        value={props.value}
        onchange={props.onchange}
        options={props.options} 
      />
  </div>
  )
}


const BacklogContainer = () => {
  const [backlogs, updateBacklogs] = React.useState([]);
  const [displayedBacklogs, updateDisplayedBacklogs] = React.useState([]);
  const [genreFilter, updateGenreFilter] = React.useState(""); 
  const [genresList, updateGenresList] = React.useState([])
  const [platformFilter, updatePlatformFilter] = React.useState("")
  const [platformsList, updatePlatformsList] = React.useState([])
  const [ownershipFilter, updateOwnershipFilter] = React.useState("")
  const [ownershipList, updateOwnershipList] = React.useState([])
  const [playstatusFilter, updatePlaystatusFilter] = React.useState("")
  const [playstatusList, updatePlaystatusList] = React.useState([])
  const [sortingChoice, updateSortingChoice] = React.useState("")
  const [sortingList, updateSortingList] = React.useState([])


  React.useEffect(() => {
    fetch("/api/backlog")
      .then((response) => response.json())
      // .then((data) => {console.log(data); return data})
      .then((data) => {
        // Load initial backlog data into component
        updateBacklogs(data);
        updateDisplayedBacklogs(data);
        console.log(backlogs)
      });
  }, []);



  React.useEffect(() => {
    let updatedList = backlogs.map((backlog) => backlog.platform)
    updatedList = new Set(updatedList)
    updatePlatformsList([...updatedList, ...platformsList])
  }, [backlogs])

  React.useEffect(() => {
    if (platformFilter === "All") {
      updateDisplayedBacklogs(backlogs)
    } else {
      let updatedDisplay = backlogs.filter((backlog) => backlog.platform === platformFilter)
    

      if (genreFilter != "") {
        updatedDisplay = updatedDisplay.filter((backlog) => backlog.genre === genreFilter);
      }

      if (ownershipFilter != "") {
        updatedDisplay = updatedDisplay.filter((backlog) => backlog.ownership_status === ownershipFilter);
      }

      if (playstatusFilter != "") {
        updatedDisplay = updatedDisplay.filter((backlog) => backlog.play_status === playstatusFilter);
      }
      updateDisplayedBacklogs(updatedDisplay)
    }
  }, [platformFilter])




  React.useEffect(() => {
    let updatedList = backlogs.map((backlog) => backlog.play_status ? 'Currently Playing' : 'Not Playing')
    updatedList = new Set(updatedList)
    updatePlaystatusList([...updatedList, ...playstatusList])
  }, [backlogs])
  
  React.useEffect(() => {
    if (playstatusFilter === 'Currently Playing') {
      updateDisplayedBacklogs(backlogs.filter((backlog) => {
        return backlog.play_status === true;
      }));
    } else if (playstatusFilter === 'Not Playing') {
      updateDisplayedBacklogs(
        backlogs.filter((backlog) => backlog.play_status === false)
      );
    } else {
      updateDisplayedBacklogs(backlogs)
    }
  }, [playstatusFilter])




  React.useEffect(() => {
    let updatedList = backlogs.map((backlog) => backlog.ownership_status)
    updatedList = new Set(updatedList)
    updateOwnershipList([...updatedList, ...ownershipList])
  }, [backlogs])

  React.useEffect(() => {
    if (ownershipFilter === "All") {
      updateDisplayedBacklogs(backlogs)
    } else {
      let updatedDisplay = backlogs.filter((backlog) => backlog.ownership_status === ownershipFilter)
      

      if (playstatusFilter != "") {
        updatedDisplay = updatedDisplay.filter((backlog) => backlog.play_status === playstatusFilter);
      }

      if (genreFilter != "") {
        updatedDisplay = updatedDisplay.filter((backlog) => backlog.genre === genreFilter);
      }

      if (platformFilter != "") {
        updatedDisplay = updatedDisplay.filter((backlog) => backlog.platform === platformFilter);
      }

      updateDisplayedBacklogs(updatedDisplay)
    }
  }, [ownershipFilter])

  

  React.useEffect(() => {
    let updatedList = backlogs.map((backlog) => backlog.genre)
    updatedList = new Set(updatedList)
    updateGenresList([...updatedList, ...genresList])
  }, [backlogs])

  React.useEffect(() => {
    if (genreFilter === "All") {
      updateDisplayedBacklogs(backlogs)
    } else {
      let updatedDisplay = backlogs.filter((backlog) => backlog.genre === genreFilter)

      if (platformFilter != "") {
        updatedDisplay = updatedDisplay.filter((backlog) => backlog.platform === platformFilter);
      }

      if (ownershipFilter != "") {
        updatedDisplay = updatedDisplay.filter((backlog) => backlog.ownership_status === ownershipFilter);
      }

      if (playstatusFilter != "") {
        updatedDisplay = updatedDisplay.filter((backlog) => backlog.play_status === playstatusFilter);
      }
      
      updateDisplayedBacklogs(updatedDisplay)
    }
  }, [genreFilter])



  

  React.useEffect(() => {
    updateSortingList(['Genre', 'Platform', 'Ownership Status', 'Play Status'])
  }, [backlogs])



  React.useEffect(() => {
    let choice = '';

    if (sortingChoice === 'Genre') {
      choice = 'genre'
    } else if (sortingChoice === 'Platform') {
      choice = 'platform'
    } else if (sortingChoice === 'Play Status') {
      choice = 'play_status'
    } else if (sortingChoice === 'Ownership Status') {
      choice = 'ownership_status'
    } else {
      choice = 'All'
    } 
    
    // console.log(sortingChoice, 'SORTING CHOICE')
    // console.log(choice, 'CHOICE')

    if (sortingChoice === "All") {
      updateDisplayedBacklogs(backlogs)
    } else {
      const updatedBacklogs = backlogs.sort((backlog1, backlog2) => {
        if (backlog1[choice] > backlog2[choice]) {
          return 1;
        } else if ((backlog1[choice] < backlog2[choice])) {
          return -1;
        } else {
          return 0;
        }
      });
      updateDisplayedBacklogs(updatedBacklogs)
      console.log(updatedBacklogs, ' UPDATED DISPLAY THAT SHOULD BE SHOWING')
    }
  }, [sortingChoice])



  React.useEffect(() => {
    console.log(displayedBacklogs)
  }, [displayedBacklogs])

  const handleSortSelect = (e) => {
    updateSortingChoice(e.target.value)
  }

  const handleSelect = (e) => {
    updateGenreFilter(e.target.value)
  }

  const handleplatformSelect = (e) => {
    updatePlatformFilter(e.target.value)
  }

  const handleOwnershipSelect = (e) => {
    updateOwnershipFilter(e.target.value)
  }

  const handlePlaystatusSelect = (e) => {
    updatePlaystatusFilter(e.target.value)
  }

  
  console.log(displayedBacklogs)

  return (
    <div>

      <div className="row">
        <div className="col-3 col-sm-2 col-md-3 col-lg-3 col-xl-2 col-xxl-2 card-transparent filters">    

          <div className="card-body mb-3">

            <h4 className="text-center card-title">Filter By:</h4>

            <div className="card-subtitle">Genre</div>
            <FilterOptions 
              value={genreFilter}
              onchange={handleSelect}
              options={genresList} 
            />

            <div className="card-subtitle">Platform</div>
            <FilterOptions 
              value={platformFilter}
              onchange={handleplatformSelect}
              options={platformsList}
            />


            <div className="card-subtitle">Ownership Status</div>
            <FilterOptions 
              value={ownershipFilter}
              onchange={handleOwnershipSelect}
              options={ownershipList}
            />

          
            <div className="card-subtitle">Play Status</div>
            <FilterOptions 
              value={playstatusFilter}
              onchange={handlePlaystatusSelect}
              options={playstatusList}

            /> <br></br>

            <h4 className="text-center card-title" id="sort-by">Sort By:</h4>
            <FilterOptions
              value={sortingChoice}
              onchange={(e) => handleSortSelect(e)}
              options={sortingList}
            />
          </div>  
        </div>  
      
        <div className="col">
          {displayedBacklogs.map(backlog => {
             return ( <BacklogEntry
              key={backlog.backlog_id}
              title={backlog.game.title}
              image= {backlog.game.image}
              genre= {backlog.genre}
              ownership_status= {backlog.ownership_status}
              play_status={backlog.play_status}
              platform={backlog.platform}
            />)
            })}
         
        </div>
      </div>    
    </div>
  )
};


ReactDOM.render(<BacklogContainer />, document.getElementById("page"));