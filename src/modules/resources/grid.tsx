import React, { useState, useEffect, SyntheticEvent } from 'react'
import { Grid as OpsGrid } from 'opsramp-design-system'
import { useResourceGrid } from 'context/resource-grid-context'
type gridProps = {
  clientId: any
}
const Grid: React.FC<gridProps> = props => {
  // console.log('Grid load!!!')
  const [rowData, setRowData] = useState<any>(null)
  const [columnDefs, setColumnDefs] = useState<any>([])
  const [gridApi, setGridApi] = useState<any>(null)
  const { state: gridContext, dispatch: gridDispatch } = useResourceGrid()

  useEffect(() => {
    if (
      gridContext.columns &&
      gridContext.columns?.selectedColumns.length > 0 &&
      gridContext.rows?.devices
    ) {
      // remove bad properties from all items before passing to ag-grid
      let cols = gridContext.columns?.selectedColumns

      cols?.map(col => {
        if (
          col.field === 'name' ||
          col.field === 'hostName' ||
          col.field === 'ipAddress' ||
          col.field === 'instanceName'
        ) {
          // apply a formatter because this should be a link, not just text
          col.cellRendererFramework = cellLink
        }

        if (col.field === 'technologies') {
          col.cellRendererFramework = technologiesCol
        }
      })

      // add 2 columns, checkbox and status
      cols?.unshift({
        field: '',
        sortable: false,
        suppressMovable: true,
        width: 5,
        lockPosition: true,
        cellRendererFramework: ourFormatterFunction
      })
      cols?.unshift({
        sortable: false,
        headerCheckboxSelection: true,
        headerCheckboxSelectionFilteredOnly: true,
        checkboxSelection: true,
        suppressMovable: true,
        width: 36,
        lockPosition: true
      })
      setColumnDefs(cols)
      setRowData(gridContext.rows?.devices)
    }
  }, [gridContext, ourFormatterFunction])

  function technologiesCol(params: any) {
    let main: any = {}
    const k = params.value
    console.log('tech col', params)

    if (k.length === 0) {
      main.iconClass = ''
      main.tip = ''
    } else {
      k.forEach((el: any) => {
        if (el.iconClass) {
          main.iconClass = el.iconClass
          main.tip = el.tip
        }
      })
    }
    return <i className={main.iconClass} title={main.tip}></i>
  }

  function cellLink(params: any) {
    let url = `/devicePage.do?id=${params.data.id}`
    return (
      <a href={url} target="_blank" title={params.value}>
        {params.value}
      </a>
    )
  }

  function ourFormatterFunction(params: any) {
    return (
      <div onClick={testFunction} className="status-div">
        <div className="status-bar"></div>
        {/* <div>Test</div> */}
      </div>
    )
  }

  function testFunction(params: any) {
    console.log('clicked')
  }

  function onGridReady(params: any) {
    console.log('onparams')
    setGridApi(params.api)
  }

  const onPageSizeChanged = (e: any) => {
    var value = e.nativeEvent.target.value
    gridApi.paginationSetPageSize(Number(value))
  }

  return (
    <div className="ag-theme-alpine w-100 h-100">
      {columnDefs && columnDefs.length > 0 && rowData && (
        <OpsGrid
          columnDefs={columnDefs}
          rowData={rowData}
          pagination={true}
          rowSelection="multiple"
          paginationPageSize={10}
          animateRows={true}
          onGridReady={onGridReady}
        ></OpsGrid>
      )}
      <select onChange={e => onPageSizeChanged(e)} id="page-size">
        <option value="10">10</option>
        <option value="20">20</option>
        <option value="30">30</option>
        <option value="40">40</option>
      </select>
    </div>
  )
}
export default Grid
