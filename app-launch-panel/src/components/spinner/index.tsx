import React from 'react'
import './index.css'
const Spinner: React.FC = () => {
  return (
    <div>
      <div className="spinner" />
      <div className="logo">loading...</div>
    </div>
  )
}

export default Spinner
