/*
 * Copyright (c) 2016 University of Miami
 */

package edu.miami.drilsdown;


import org.ramadda.repository.*;
import org.ramadda.repository.output.*;
import org.ramadda.repository.type.*;
import org.ramadda.util.HtmlUtils;
import org.ramadda.util.Json;
import org.ramadda.util.Utils;

import org.w3c.dom.Element;

import ucar.unidata.util.StringUtil;
import java.util.ArrayList;
import java.util.Hashtable;
import java.util.List;




/**
 */
public class DrilsdownApiHandler extends RepositoryManager implements RequestHandler {


    /**
     * _more_
     *
     * @param repository _more_
     * @param node _more_
     * @param props _more_
     *
     * @throws Exception _more_
     */
    public DrilsdownApiHandler(Repository repository, Element node,
                             Hashtable props)
            throws Exception {
        super(repository);
    }

    public Result processTest(Request request) throws Exception {
        return new Result("Hello", new StringBuilder("drilsdown api test"));
    }

    public Result processGetBundle(Request request) throws Exception {
        Entry              entry = getEntryManager().getEntryFromArg(request, ARG_ENTRYID);
        if(entry == null) {
            throw new RepositoryUtil.MissingEntryException("Could not find entry from entryid");
        }
        
        Entry bundleEntry = null;


        if(!entry.getTypeHandler().isType("type_idv_bundle")) {
            for (Entry child : getEntryManager().getChildren(request, entry)) {
                if(child.getTypeHandler().isType("type_idv_bundle")) {
                    bundleEntry = child;
                    break;
                }
            }
        } else {
            bundleEntry = entry;
        }
        if(bundleEntry == null) {
            throw new RepositoryUtil.MissingEntryException("Could not find entry");
        }

        return getEntryManager().processEntryGet(request, bundleEntry);
    }



}
