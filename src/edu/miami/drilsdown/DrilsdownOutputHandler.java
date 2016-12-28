/*
 * Copyright (c) 2008-2016 Geode Systems LLC
 * This Software is licensed under the Geode Systems RAMADDA License available in the source distribution in the file 
 * ramadda_license.txt. The above copyright notice shall be included in all copies or substantial portions of the Software.
 */

package edu.miami.drilsdown;


import org.ramadda.repository.Entry;
import org.ramadda.repository.Link;
import org.ramadda.repository.Repository;
import org.ramadda.repository.RepositoryUtil;
import org.ramadda.repository.Request;
import org.ramadda.repository.Result;
import org.ramadda.repository.map.*;
import org.ramadda.repository.metadata.ContentMetadataHandler;
import org.ramadda.repository.metadata.Metadata;
import org.ramadda.repository.output.OutputHandler;
import org.ramadda.repository.output.OutputType;


import org.ramadda.repository.type.TypeHandler;
import org.ramadda.util.HtmlUtils;
import org.ramadda.util.SelectionRectangle;

import org.w3c.dom.Element;

import ucar.unidata.util.IOUtil;



import java.io.File;

import java.util.List;


/**
 */
public class DrilsdownOutputHandler extends OutputHandler {


    /** The OutputType definition */
    public static final OutputType OUTPUT_ISL =
        new OutputType("Geolocated IDV ISL", "idv.isl",
                       OutputType.TYPE_OTHER, "", "/idv/idv.gif");


    /** The OutputType definition */
    public static final OutputType OUTPUT_ISLFORM =
        new OutputType("Geolocated IDV ISL Form", "idv.islform",
                       OutputType.TYPE_OTHER, "", "/idv/idv.gif");


    /**
     * Create an IdvWebstartOutputHandler
     *
     * @param repository  the repository
     * @param element     the Entry to serve
     * @throws Exception  problem creating handler
     */
    public DrilsdownOutputHandler(Repository repository, Element element)
            throws Exception {
        super(repository, element);
        addType(OUTPUT_ISL);
        addType(OUTPUT_ISLFORM);
    }



    /**
     * Get the entry links
     *
     * @param request  the Request
     * @param state    the Entry
     * @param links    the list of links to add to
     *
     * @throws Exception  problems
     */
    public void getEntryLinks(Request request, State state, List<Link> links)
            throws Exception {

        Entry entry = state.getEntry();
        if (entry == null) {
            return;
        }
        if (entry.getResource().getPath().endsWith(".xidv")
                || entry.getResource().getPath().endsWith(".zidv")) {
            String fileTail = getStorageManager().getFileTail(entry);
            String suffix   = "/" + IOUtil.stripExtension(fileTail) + ".isl";
            //                suffix = java.net.URLEncoder.encode(suffix);
            links.add(makeLink(request, state.getEntry(), OUTPUT_ISLFORM,
                               suffix));
            links.add(makeLink(request, state.getEntry(), OUTPUT_ISL,
                               suffix));
        }
    }


    /**
     * Output a group
     *
     * @param request     the Request
     * @param outputType  the OutputType
     * @param group       the group to output
     * @param subGroups   subgroups
     * @param entries     list of Entrys
     *
     * @return  the Result
     *
     * @throws Exception  problems
     */
    public Result outputGroup(Request request, OutputType outputType,
                              Entry group, List<Entry> subGroups,
                              List<Entry> entries)
            throws Exception {
        return outputEntry(request, outputType, group);
    }

    /**
     * _more_
     *
     * @param request _more_
     * @param outputType _more_
     * @param entry _more_
     *
     * @return _more_
     *
     * @throws Exception _more_
     */
    public Result outputEntryForm(Request request, OutputType outputType,
                                  Entry entry)
            throws Exception {
        if (request.exists(ARG_SUBMIT)) {
            return outputEntryIsl(request, outputType, entry);
        }
        StringBuilder sb = new StringBuilder();
        getPageHandler().entrySectionOpen(request, entry, sb, "IDV ISL Form");
        String formUrl = request.entryUrl(getRepository().URL_ENTRY_SHOW,
                                          entry);
        String formId = HtmlUtils.getUniqueId("form_");
        sb.append(HtmlUtils.form(formUrl, HtmlUtils.id(formId)));
        sb.append(HtmlUtils.hidden(ARG_ENTRYID, entry.getId()));
        sb.append(HtmlUtils.hidden(ARG_OUTPUT, OUTPUT_ISLFORM.toString()));
        sb.append(HtmlUtils.formTable());
        SelectionRectangle bbox = TypeHandler.getSelectionBounds(request);
        MapInfo map = getRepository().getMapManager().createMap(request,
                          true, null);

        String mapSelector = map.makeSelector("bounds", true,
                                 bbox.getStringArray(), "", "");
        sb.append(formEntry(request, msgLabel("Area"), mapSelector));
        sb.append(HtmlUtils.submit(msg("Make ISL"), ARG_SUBMIT));
        sb.append(HtmlUtils.formTableClose());

        sb.append(HtmlUtils.formClose());
        //        OutputHandler.addUrlShowingForm(sb, formId, null);
        getPageHandler().entrySectionClose(request, entry, sb);

        Result result = new Result("", sb);

        return result;
    }


    /**
     * Output an Entry
     *
     * @param request     the Request
     * @param outputType  type of Output
     * @param entry       the Entry
     *
     * @return  the Result
     *
     * @throws Exception problems
     */
    public Result outputEntry(Request request, OutputType outputType,
                              Entry entry)
            throws Exception {
        if (outputType.equals(OUTPUT_ISLFORM)) {
            return outputEntryForm(request, outputType, entry);
        }

        return outputEntryIsl(request, outputType, entry);
    }

    /**
     * _more_
     *
     * @param request _more_
     * @param outputType _more_
     * @param entry _more_
     *
     * @return _more_
     *
     * @throws Exception _more_
     */
    public Result outputEntryIsl(Request request, OutputType outputType,
                                 Entry entry)
            throws Exception {


        StringBuilder isl      = new StringBuilder();


        String        fileTail = getStorageManager().getFileTail(entry);
        String url =
            HtmlUtils.url(request.makeUrl(getRepository().URL_ENTRY_GET)
                          + "/" + fileTail, ARG_ENTRYID, entry.getId());
        url = request.getAbsoluteUrl(url);
        isl.append("<isl>\n<bundle file=\"");
        isl.append(url);
        isl.append("\" ");
        System.err.println("bounds:" + request);
        String north = request.getString("north",
                                         request.getString("bounds_north",
                                             "90"));
        String west = request.getString("west",
                                        request.getString("bounds_west",
                                            "-180"));
        String south = request.getString("south",
                                         request.getString("bounds_south",
                                             "-90"));
        String east = request.getString("east",
                                        request.getString("bounds_east",
                                            "180"));
        isl.append("bbox=\"" + north + "," + west + "," + south + "," + east
                   + "\"");
        isl.append("/>\n");
        isl.append("<pause/>\n");
        isl.append("<center north=\"" + north + "\" west=\"" + west
                   + "\" south=\"" + south + "\" east=\"" + east + "\" />\n");
        isl.append("</isl>\n");
        Result result = new Result("", isl, "application/x-idv-isl");
        result.setReturnFilename(fileTail + ".isl");

        return result;
    }



}
