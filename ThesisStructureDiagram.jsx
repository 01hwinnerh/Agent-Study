import React from 'react';

const ThesisStructureDiagram = () => {
  return (
    <div className="w-full max-w-4xl mx-auto p-8 bg-white font-sans text-gray-800">
      <h2 className="text-center text-xl font-bold mb-6">图 1-X 全文组织结构</h2>
      
      {/* 整体外层容器 */}
      <div className="flex flex-col gap-6 relative">
        
        {/* ================= 第一部分：研究背景与现状 ================= */}
        <div className="flex w-full">
          {/* 左侧标签 */}
          <div className="w-12 shrink-0 flex items-center justify-center relative">
            <div className="absolute inset-y-0 right-0 w-px bg-gray-400"></div>
            <div className="bg-[#f5e6d3] border border-gray-600 px-2 py-8 shadow-sm flex items-center justify-center z-10 w-10">
              <span className="writing-vertical text-center font-bold tracking-widest text-sm" style={{ writingMode: 'vertical-rl' }}>
                研究背景与现状
              </span>
            </div>
          </div>

          {/* 右侧内容区 */}
          <div className="flex-1 pl-6">
            <div className="border border-dashed border-gray-400 bg-gray-50/50 p-5 relative">
              
              {/* 第一章 */}
              <div className="mb-6">
                <div className="bg-[#cce2ff] border border-gray-600 text-center py-2 font-bold shadow-sm mx-auto w-3/4 mb-4 relative z-10">
                  第一章 绪论
                </div>
                
                {/* 连线与分支内容 */}
                <div className="flex justify-between items-start relative mt-6">
                  {/* 连接线 */}
                  <div className="absolute top-[-16px] left-1/2 w-[66%] -translate-x-1/2 h-4 border-t border-l border-r border-gray-400 z-0"></div>
                  <div className="absolute top-[-16px] left-1/2 w-px h-4 bg-gray-400 z-0"></div>

                  <div className="flex flex-col items-center w-1/3 px-2 z-10">
                    <div className="bg-[#f5e6d3] border border-gray-600 py-1.5 px-3 w-full text-center text-sm font-semibold shadow-sm mb-2">研究背景</div>
                    <div className="bg-white border border-gray-400 py-1 px-2 w-full text-center text-xs text-gray-700">分布式深度神经网络训练</div>
                  </div>
                  
                  <div className="flex flex-col items-center w-1/3 px-2 z-10">
                    <div className="bg-[#f5e6d3] border border-gray-600 py-1.5 px-3 w-full text-center text-sm font-semibold shadow-sm mb-2">研究意义</div>
                    <div className="bg-white border border-gray-400 py-1 px-2 w-full text-center text-xs text-gray-700">改善异构场景下的资源利用率</div>
                  </div>
                  
                  <div className="flex flex-col items-center w-1/3 px-2 z-10">
                    <div className="bg-[#f5e6d3] border border-gray-600 py-1.5 px-3 w-full text-center text-sm font-semibold shadow-sm mb-2">研究内容</div>
                    <div className="bg-white border border-gray-400 py-1 px-2 w-full text-center text-xs text-gray-700">集群网络的负载均衡策略</div>
                  </div>
                </div>
              </div>

              {/* 第二章 */}
              <div className="mt-8 pt-6 border-t border-gray-300 border-dashed relative">
                {/* 向下的箭头 */}
                <div className="absolute top-0 left-1/2 -translate-x-1/2 -mt-2 w-0 h-0 border-l-4 border-r-4 border-t-[6px] border-l-transparent border-r-transparent border-t-gray-500"></div>
                
                <div className="bg-[#cce2ff] border border-gray-600 text-center py-2 font-bold shadow-sm mx-auto w-3/4 mb-5 relative z-10">
                  第二章 研究现状
                </div>
                
                <div className="flex justify-around items-start relative mt-4">
                   <div className="absolute top-[-10px] left-1/2 w-[50%] -translate-x-1/2 h-[10px] border-t border-l border-r border-gray-400 z-0"></div>

                  <div className="flex flex-col items-center w-5/12 z-10">
                    <div className="bg-[#f5e6d3] border border-gray-600 py-2 px-4 w-full text-center text-sm font-semibold shadow-sm mb-3">分布式训练通信优化</div>
                    <div className="flex flex-col gap-1 w-4/5">
                      <div className="bg-white border border-gray-400 py-1 px-2 w-full text-center text-xs">流水线调度</div>
                      <div className="bg-white border border-gray-400 py-1 px-2 w-full text-center text-xs">梯度压缩</div>
                      <div className="bg-white border border-gray-400 py-1 px-2 w-full text-center text-xs">网内聚合</div>
                      <div className="bg-white border border-gray-400 py-1 px-2 w-full text-center text-xs">网络传输</div>
                    </div>
                  </div>

                  <div className="flex flex-col items-center w-5/12 z-10">
                    <div className="bg-[#f5e6d3] border border-gray-600 py-2 px-4 w-full text-center text-sm font-semibold shadow-sm mb-3">负载均衡</div>
                    <div className="flex flex-col gap-1 w-4/5">
                      <div className="bg-white border border-gray-400 py-1 px-2 w-full text-center text-xs">流粒度</div>
                      <div className="bg-white border border-gray-400 py-1 px-2 w-full text-center text-xs">包粒度</div>
                      <div className="bg-white border border-gray-400 py-1 px-2 w-full text-center text-xs">流片粒度</div>
                    </div>
                  </div>
                </div>
              </div>

            </div>
          </div>
        </div>

        {/* 区域间连接箭头 */}
        <div className="flex justify-center -my-2 relative z-20">
            <div className="w-0 h-0 border-l-[8px] border-r-[8px] border-t-[12px] border-l-transparent border-r-transparent border-t-gray-500"></div>
        </div>

        {/* ================= 第二部分：研究过程 ================= */}
        <div className="flex w-full">
          {/* 左侧标签 */}
          <div className="w-12 shrink-0 flex items-center justify-center relative">
            <div className="absolute inset-y-0 right-0 w-px bg-gray-400"></div>
            <div className="bg-[#f5e6d3] border border-gray-600 px-2 py-8 shadow-sm flex items-center justify-center z-10 w-10">
              <span className="writing-vertical text-center font-bold tracking-widest text-sm" style={{ writingMode: 'vertical-rl' }}>
                研究过程
              </span>
            </div>
          </div>

          {/* 右侧内容区 */}
          <div className="flex-1 pl-6">
            <div className="border border-dashed border-gray-400 bg-gray-50/50 p-5 flex gap-6 relative">
              
              {/* 第三章 */}
              <div className="flex-1 flex flex-col items-center border border-gray-200 bg-white p-4 shadow-sm relative">
                <div className="bg-[#cce2ff] border border-gray-600 text-center py-2 px-3 font-bold shadow-sm w-full mb-6 min-h-[60px] flex items-center justify-center text-sm">
                  第三章 针对分布式训练梯度同步优化的负载均衡机制
                </div>
                
                <div className="w-full flex items-center mb-4 relative">
                  <div className="w-24 shrink-0 bg-[#f5e6d3] border border-gray-600 py-1.5 text-center text-sm font-semibold z-10">问题分析</div>
                  <div className="flex-1 border-t border-gray-400 relative">
                     <div className="absolute right-0 top-1/2 -translate-y-1/2 w-0 h-0 border-t-4 border-b-4 border-l-[6px] border-t-transparent border-b-transparent border-l-gray-500"></div>
                  </div>
                  <div className="w-32 shrink-0 bg-white border border-gray-400 py-1.5 text-center text-xs ml-2">梯度同步延迟</div>
                </div>

                <div className="w-px h-6 bg-gray-400 -mt-4 mb-2 ml-[-120px]"></div>
                <div className="w-0 h-0 border-l-4 border-r-4 border-t-[6px] border-l-transparent border-r-transparent border-t-gray-500 mb-2 ml-[-120px]"></div>

                <div className="w-full flex items-center mb-4 relative">
                  <div className="w-24 shrink-0 bg-[#f5e6d3] border border-gray-600 py-1.5 text-center text-sm font-semibold z-10">总体设计</div>
                  <div className="w-4 border-t border-gray-400"></div>
                  <div className="w-px h-10 bg-gray-400"></div>
                  <div className="flex flex-col justify-between h-12 ml-2 flex-1 relative">
                    <div className="flex items-center">
                      <div className="w-3 border-t border-gray-400 relative">
                         <div className="absolute right-0 top-1/2 -translate-y-1/2 w-0 h-0 border-t-[3px] border-b-[3px] border-l-[5px] border-t-transparent border-b-transparent border-l-gray-500"></div>
                      </div>
                      <div className="w-full bg-white border border-gray-400 py-1 text-center text-xs ml-1">路径选择</div>
                    </div>
                    <div className="flex items-center">
                      <div className="w-3 border-t border-gray-400 relative">
                         <div className="absolute right-0 top-1/2 -translate-y-1/2 w-0 h-0 border-t-[3px] border-b-[3px] border-l-[5px] border-t-transparent border-b-transparent border-l-gray-500"></div>
                      </div>
                      <div className="w-full bg-white border border-gray-400 py-1 text-center text-xs ml-1">传输协议</div>
                    </div>
                  </div>
                </div>

                <div className="w-px h-6 bg-gray-400 -mt-4 mb-2 ml-[-120px]"></div>
                <div className="w-0 h-0 border-l-4 border-r-4 border-t-[6px] border-l-transparent border-r-transparent border-t-gray-500 mb-2 ml-[-120px]"></div>

                <div className="w-full flex items-center relative">
                  <div className="w-24 shrink-0 bg-[#f5e6d3] border border-gray-600 py-1.5 text-center text-sm font-semibold z-10">性能评估</div>
                  <div className="flex-1 border-t border-gray-400 relative">
                     <div className="absolute right-0 top-1/2 -translate-y-1/2 w-0 h-0 border-t-4 border-b-4 border-l-[6px] border-t-transparent border-b-transparent border-l-gray-500"></div>
                  </div>
                  <div className="w-32 shrink-0 bg-white border border-gray-400 py-1.5 text-center text-xs ml-2">聚合迭代时间</div>
                </div>
              </div>

              {/* 第四章 */}
              <div className="flex-1 flex flex-col items-center border border-gray-200 bg-white p-4 shadow-sm relative">
                <div className="bg-[#cce2ff] border border-gray-600 text-center py-2 px-3 font-bold shadow-sm w-full mb-6 min-h-[60px] flex items-center justify-center text-sm">
                  第四章 分布式机器学习混合并行模式感知的负载均衡机制
                </div>
                
                <div className="w-full flex items-center mb-4 relative">
                  <div className="w-24 shrink-0 bg-[#f5e6d3] border border-gray-600 py-1.5 text-center text-sm font-semibold z-10">问题分析</div>
                  <div className="flex-1 border-t border-gray-400 relative">
                     <div className="absolute right-0 top-1/2 -translate-y-1/2 w-0 h-0 border-t-4 border-b-4 border-l-[6px] border-t-transparent border-b-transparent border-l-gray-500"></div>
                  </div>
                  <div className="w-32 shrink-0 bg-white border border-gray-400 py-1.5 text-center text-xs ml-2">异构流量竞争</div>
                </div>

                <div className="w-px h-6 bg-gray-400 -mt-4 mb-2 ml-[-120px]"></div>
                <div className="w-0 h-0 border-l-4 border-r-4 border-t-[6px] border-l-transparent border-r-transparent border-t-gray-500 mb-2 ml-[-120px]"></div>

                <div className="w-full flex items-center mb-4 relative">
                  <div className="w-24 shrink-0 bg-[#f5e6d3] border border-gray-600 py-1.5 text-center text-sm font-semibold z-10">总体设计</div>
                  <div className="w-4 border-t border-gray-400"></div>
                  <div className="w-px h-10 bg-gray-400"></div>
                  <div className="flex flex-col justify-between h-12 ml-2 flex-1 relative">
                    <div className="flex items-center">
                      <div className="w-3 border-t border-gray-400 relative">
                         <div className="absolute right-0 top-1/2 -translate-y-1/2 w-0 h-0 border-t-[3px] border-b-[3px] border-l-[5px] border-t-transparent border-b-transparent border-l-gray-500"></div>
                      </div>
                      <div className="w-full bg-white border border-gray-400 py-1 text-center text-xs ml-1">模式识别</div>
                    </div>
                    <div className="flex items-center">
                      <div className="w-3 border-t border-gray-400 relative">
                         <div className="absolute right-0 top-1/2 -translate-y-1/2 w-0 h-0 border-t-[3px] border-b-[3px] border-l-[5px] border-t-transparent border-b-transparent border-l-gray-500"></div>
                      </div>
                      <div className="w-full bg-white border border-gray-400 py-1 text-center text-xs ml-1">差异选路</div>
                    </div>
                  </div>
                </div>

                <div className="w-px h-6 bg-gray-400 -mt-4 mb-2 ml-[-120px]"></div>
                <div className="w-0 h-0 border-l-4 border-r-4 border-t-[6px] border-l-transparent border-r-transparent border-t-gray-500 mb-2 ml-[-120px]"></div>

                <div className="w-full flex items-center relative">
                  <div className="w-24 shrink-0 bg-[#f5e6d3] border border-gray-600 py-1.5 text-center text-sm font-semibold z-10">性能评估</div>
                  <div className="flex-1 border-t border-gray-400 relative">
                     <div className="absolute right-0 top-1/2 -translate-y-1/2 w-0 h-0 border-t-4 border-b-4 border-l-[6px] border-t-transparent border-b-transparent border-l-gray-500"></div>
                  </div>
                  <div className="w-32 shrink-0 bg-white border border-gray-400 py-1.5 text-center text-xs ml-2">集群训练效率</div>
                </div>
              </div>

            </div>
          </div>
        </div>

        {/* 区域间连接箭头 */}
        <div className="flex justify-center -my-2 relative z-20">
            <div className="w-0 h-0 border-l-[8px] border-r-[8px] border-t-[12px] border-l-transparent border-r-transparent border-t-gray-500"></div>
        </div>

        {/* ================= 第三部分：研究结论 ================= */}
        <div className="flex w-full">
          {/* 左侧标签 */}
          <div className="w-12 shrink-0 flex items-center justify-center relative">
            <div className="absolute inset-y-0 right-0 w-px bg-gray-400"></div>
            <div className="bg-[#f5e6d3] border border-gray-600 px-2 py-6 shadow-sm flex items-center justify-center z-10 w-10">
              <span className="writing-vertical text-center font-bold tracking-widest text-sm" style={{ writingMode: 'vertical-rl' }}>
                研究结论
              </span>
            </div>
          </div>

          {/* 右侧内容区 */}
          <div className="flex-1 pl-6">
            <div className="border border-dashed border-gray-400 bg-gray-50/50 p-4 relative">
              <div className="bg-[#cce2ff] border border-gray-600 text-center py-3 font-bold shadow-sm w-full relative z-10">
                第五章 总结与展望
              </div>
            </div>
          </div>
        </div>

      </div>
    </div>
  );
};

export default ThesisStructureDiagram;