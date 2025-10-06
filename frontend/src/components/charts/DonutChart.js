import React, { useEffect, useRef } from 'react';
import * as d3 from 'd3';

function DonutChart({ data, width = 400, height = 300, margin = { top: 20, right: 20, bottom: 20, left: 20 } }) {
  const svgRef = useRef();

  useEffect(() => {
    if (!data || !data.length) return;

    // Clear any existing SVG
    d3.select(svgRef.current).selectAll('*').remove();

    const radius = Math.min(width - margin.left - margin.right, height - margin.top - margin.bottom) / 2;

    // Create color scale
    const color = d3.scaleOrdinal()
      .domain(data.map(d => d.label))
      .range(d3.schemeCategory10);

    // Create pie layout
    const pie = d3.pie()
      .value(d => d.value)
      .sort(null);

    // Create arc generator
    const arc = d3.arc()
      .innerRadius(radius * 0.6) // Create donut hole
      .outerRadius(radius);

    // Create SVG
    const svg = d3.select(svgRef.current)
      .attr('width', width)
      .attr('height', height)
      .append('g')
      .attr('transform', `translate(${width / 2},${height / 2})`);

    // Add arcs
    const arcs = svg.selectAll('arc')
      .data(pie(data))
      .enter()
      .append('g')
      .attr('class', 'arc');

    arcs.append('path')
      .attr('d', arc)
      .attr('fill', d => color(d.data.label))
      .attr('stroke', 'white')
      .style('stroke-width', '2px')
      .style('opacity', 0.8)
      .on('mouseover', function() {
        d3.select(this)
          .style('opacity', 1);
      })
      .on('mouseout', function() {
        d3.select(this)
          .style('opacity', 0.8);
      });

    // Add labels
    const arcLabel = d3.arc()
      .innerRadius(radius * 0.8)
      .outerRadius(radius * 0.8);

    arcs.append('text')
      .attr('transform', d => `translate(${arcLabel.centroid(d)})`)
      .attr('dy', '0.35em')
      .attr('text-anchor', 'middle')
      .text(d => d.data.label)
      .style('font-size', '12px')
      .style('fill', 'white');

    // Add center text
    svg.append('text')
      .attr('text-anchor', 'middle')
      .attr('dy', '0.35em')
      .style('font-size', '16px')
      .text('Transit Types');

  }, [data, width, height, margin]);

  return <svg ref={svgRef} />;
}

export default DonutChart;